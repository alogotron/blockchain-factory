// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Script.sol";
import "../src/ShutterZkTLSGateway.sol";

contract DeployShutterZkTLSGateway is Script {
    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerKey);

        console.log("Deployer:", deployer);
        console.log("Chain ID:", block.chainid);

        vm.startBroadcast(deployerKey);

        // Deploy with no claim verifier initially (can be set later)
        ShutterZkTLSGateway gateway = new ShutterZkTLSGateway(address(0));

        console.log("ShutterZkTLSGateway deployed at:", address(gateway));
        console.log("Owner:", gateway.owner());

        vm.stopBroadcast();
    }
}
