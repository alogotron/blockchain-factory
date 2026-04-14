"""EM8128Client — Execution Market signed API client.
Usage:
    from em_client import EM8128Client, get_client
    import asyncio
    client = get_client()          # uses Alpha wallet from config.json
    result = asyncio.run(client.get('/api/v1/public/metrics'))
"""
import asyncio, base64, hashlib, json, time
from pathlib import Path
from urllib.parse import urlparse
from eth_account import Account
from eth_account.messages import encode_defunct
import httpx

SKILL_DIR = Path.home() / '.openclaw' / 'skills' / 'execution-market'
API_URL   = 'https://api.execution.market'


class EM8128Client:
    def __init__(self, private_key: str, chain_id: int = 8453, api_url: str = API_URL):
        self.account     = Account.from_key(private_key)
        self.wallet      = self.account.address
        self.chain_id    = chain_id
        self.api_url     = api_url
        self.private_key = private_key

    def _build_sig_params(self, covered, params):
        comp_str = ' '.join(f'"{c}"' for c in covered)
        parts = [f'({comp_str})']
        for key in ['created', 'expires', 'nonce', 'keyid']:
            if key in params:
                v = params[key]
                parts.append(f'{key}={v}' if isinstance(v, int) else f'{key}="{v}"')
        for key in sorted(params):
            if key not in ['created', 'expires', 'nonce', 'keyid']:
                v = params[key]
                parts.append(f'{key}={v}' if isinstance(v, int) else f'{key}="{v}"')
        return ';'.join(parts)

    async def _sign_headers(self, method, url, body=None):
        async with httpx.AsyncClient() as c:
            nonce = (await c.get(f'{self.api_url}/api/v1/auth/nonce')).json()['nonce']
        parsed  = urlparse(url)
        created = int(time.time())
        covered = ['@method', '@authority', '@path']
        content_digest = None
        if parsed.query:
            covered.append('@query')
        if body:
            b = body.encode() if isinstance(body, str) else body
            b64 = base64.b64encode(hashlib.sha256(b).digest()).decode()
            content_digest = f'sha-256=:{b64}:'
            covered.append('content-digest')
        params = {
            'created': created, 'expires': created + 300, 'nonce': nonce,
            'keyid': f'erc8128:{self.chain_id}:{self.wallet}', 'alg': 'eip191'
        }
        lines = []
        for comp in covered:
            if   comp == '@method':         lines.append(f'"@method": {method.upper()}')
            elif comp == '@authority':      lines.append(f'"@authority": {parsed.netloc}')
            elif comp == '@path':           lines.append(f'"@path": {parsed.path}')
            elif comp == '@query':          lines.append(f'"@query": ?{parsed.query}')
            elif comp == 'content-digest': lines.append(f'"content-digest": {content_digest}')
        sp = self._build_sig_params(covered, params)
        lines.append(f'"@signature-params": {sp}')
        msg    = encode_defunct(text='\n'.join(lines))
        signed = Account.sign_message(msg, self.private_key)
        sig_b64 = base64.b64encode(signed.signature).decode()
        headers = {'Signature': f'eth=:{sig_b64}:', 'Signature-Input': f'eth={sp}'}
        if content_digest:
            headers['Content-Digest'] = content_digest
        return headers

    async def get(self, path):
        url  = f'{self.api_url}{path}'
        auth = await self._sign_headers('GET', url)
        async with httpx.AsyncClient(timeout=30) as c:
            return (await c.get(url, headers=auth)).json()

    async def post(self, path, data=None):
        url  = f'{self.api_url}{path}'
        body = json.dumps(data) if data else None
        auth = await self._sign_headers('POST', url, body)
        headers = {'Content-Type': 'application/json', **auth}
        async with httpx.AsyncClient(timeout=60) as c:
            return (await c.post(url, content=body, headers=headers)).json()

    async def patch(self, path, data=None):
        url  = f'{self.api_url}{path}'
        body = json.dumps(data) if data else None
        auth = await self._sign_headers('PATCH', url, body)
        headers = {'Content-Type': 'application/json', **auth}
        async with httpx.AsyncClient(timeout=60) as c:
            return (await c.patch(url, content=body, headers=headers)).json()


def get_client(wallet_name: str = 'alpha') -> EM8128Client:
    """Load client from config.json. Expects private_key stored there."""
    cfg = json.loads((SKILL_DIR / 'config.json').read_text())
    key = cfg.get('private_key')
    if not key:
        raise ValueError('No private_key in config.json — add it or pass directly')
    return EM8128Client(private_key=key, chain_id=8453)


def save_task(task: dict):
    """Append a task to active-tasks.json tracker."""
    tracker = SKILL_DIR / 'active-tasks.json'
    data = json.loads(tracker.read_text()) if tracker.exists() else {'tasks': []}
    data['tasks'].append({
        'id':          task.get('id'),
        'title':       task.get('title'),
        'status':      task.get('status', 'published'),
        'deadline':    task.get('deadline'),
        'bounty_usd':  task.get('bounty_usd'),
        'payment_network': task.get('payment_network', 'base'),
    })
    tracker.write_text(json.dumps(data, indent=2))


def remove_task(task_id: str):
    """Remove completed/cancelled task from tracker."""
    tracker = SKILL_DIR / 'active-tasks.json'
    if not tracker.exists():
        return
    data = json.loads(tracker.read_text())
    data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
    tracker.write_text(json.dumps(data, indent=2))


if __name__ == '__main__':
    async def main():
        c = get_client()
        m = await c.get('/api/v1/public/metrics')
        print(json.dumps(m, indent=2))
    asyncio.run(main())
