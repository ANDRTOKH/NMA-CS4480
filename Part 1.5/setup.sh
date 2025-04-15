#!/bin/bash

echo "=== STEP 1: Building and Starting the Network ==="
sudo docker compose up -d
echo "Waiting for containers to fully start..."
sleep 5

echo "=== STEP 2: Installing FRR on Routers ==="
./install-frr.sh
echo "Waiting for FRR to initialize..."
sleep 5

echo "=== STEP 3: Configuring OSPF on Routers ==="
./configure-all-ospf.sh
echo "Waiting for OSPF to converge..."
sleep 10

echo "=== STEP 4: Configuring Host Routes ==="
./configure-host-routes.sh
echo "Waiting for routes to be applied..."
sleep 2

echo "=== STEP 5: Testing Connectivity ==="
./test-connectivity.sh

echo ""
echo "Setup complete! Network should now be fully operational."
