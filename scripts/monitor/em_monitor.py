#!/usr/bin/env python3
"""Execution Market monitor — checks for open tasks and new submissions.
Run manually or via cron:
    */5 * * * * python3 /a0/usr/projects/blockchain-factory/scripts/monitor/em_monitor.py
"""
import asyncio, json, sys
from pathlib import Path

# Add em_client to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tx' / 'execution-market'))
from em_client import EM8128Client, SKILL_DIR

ALPHA_KEY  = None  # loaded from config
API        = 'https://api.execution.market'
WATCH_CATS = ['code_execution', 'api_integration', 'data_processing',
               'research', 'multi_step_workflow', 'content_generation']


def load_config():
    cfg_path = SKILL_DIR / 'config.json'
    if not cfg_path.exists():
        raise FileNotFoundError(f'Config not found: {cfg_path}')
    return json.loads(cfg_path.read_text())


async def check_open_tasks(client: EM8128Client):
    """Check for published tasks we can apply to as executor."""
    import httpx, ssl
    ctx = ssl.create_default_context()
    # Public endpoint — no auth needed
    import urllib.request
    url = f'{API}/api/v1/tasks?status=published&limit=50'
    req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
    try:
        res = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = json.loads(res.read())
    except Exception as e:
        print(f'  [tasks] Error: {e}')
        return []

    tasks = data.get('tasks', data.get('items', []))
    if not tasks:
        print('  [tasks] No published tasks right now')
        return []

    relevant = [t for t in tasks if t.get('category') in WATCH_CATS]
    all_tasks = tasks

    print(f'  [tasks] {len(tasks)} published total | {len(relevant)} in our target categories')
    for t in all_tasks[:10]:
        marker = '★' if t.get('category') in WATCH_CATS else ' '
        print(f'  {marker} ${t.get("bounty_usd"):>6} [{t.get("category","?")}] {t.get("title","")[:65]}')
        print(f'         id={t.get("id")} net={t.get("payment_network")} deadline={t.get("deadline","")[:16]}')
    return relevant


async def check_active_tasks(client: EM8128Client):
    """Check status of our active published tasks."""
    tracker = SKILL_DIR / 'active-tasks.json'
    if not tracker.exists():
        return
    data = json.loads(tracker.read_text())
    if not data.get('tasks'):
        print('  [active] No active tasks in tracker')
        return

    print(f'  [active] {len(data["tasks"])} tracked tasks:')
    for t in data['tasks']:
        tid = t['id']
        detail = await client.get(f'/api/v1/tasks/{tid}')
        status = detail.get('status', '?')
        subs   = detail.get('submission_count', 0)
        apps   = detail.get('application_count', 0)
        print(f'    [{status}] {t.get("title",tid)[:50]} | apps={apps} subs={subs} bounty=${t.get("bounty_usd")}')

        # Check submissions
        if subs > 0:
            sub_data = await client.get(f'/api/v1/tasks/{tid}/submissions')
            for s in sub_data.get('submissions', []):
                score = s.get('pre_check_score', 0)
                print(f'      → Submission {s["id"][:8]}... score={score} status={s.get("status")}')
                print(f'        ⚠ REVIEW NEEDED at https://execution.market/tasks/{tid}')


async def check_metrics():
    """Quick platform health check."""
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    url = f'{API}/api/v1/public/metrics'
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req, context=ctx, timeout=10)
    m = json.loads(res.read())
    t = m.get('tasks', {})
    u = m.get('users', {})
    print(f'  [metrics] published={t.get("published")} live={t.get("live")} '
          f'completed={t.get("completed")} workers={u.get("registered_workers")} '
          f'volume=${m.get("payments",{}).get("total_volume_usd")}')


async def main():
    print('=== Execution Market Monitor ===')
    cfg = load_config()
    key = cfg.get('private_key')
    if not key:
        print('ERROR: No private_key in config.json')
        sys.exit(1)

    client = EM8128Client(private_key=key, chain_id=8453)
    print(f'  Wallet: {client.wallet}')
    print(f'  Agent:  #{cfg.get("agent_id", "?")} on {cfg.get("registered_network", "base")}')
    print()

    await check_metrics()
    print()
    await check_open_tasks(client)
    print()
    await check_active_tasks(client)
    print()
    print('=== Done ===')


if __name__ == '__main__':
    asyncio.run(main())
