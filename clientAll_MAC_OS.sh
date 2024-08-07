#!/bin/bash

# Define common parameters
BOOTSTRAP_IP="127.0.0.1"
BOOTSTRAP_PORT=5555
# NODE_IP="127.0.0.1"

# Define unique parameters for each client
CLIENTS=(
  "127.0.0.1 6001 node1 ./drive1"
  "0.0.0.0 6002 node2 ./drive2"
  "127.0.0.1 6003 node3 ./drive3"
  "0.0.0.0 6004 node4 ./drive4"
)

# Function to start client in a new terminal
start_client() {
  local NODE_IP=$1
  local NODE_PORT=$2
  local NODE_NAME=$3
  local SERVE_PATH=$4
  local CURRENT_DIR=$(pwd)
  osascript -e "tell application \"Terminal\" to do script \"cd $CURRENT_DIR && ../venv/bin/python3 src/ClientApp.py $BOOTSTRAP_IP $BOOTSTRAP_PORT $NODE_IP $NODE_PORT $NODE_NAME $SERVE_PATH\""
}
cd /Users/rasikamaduranga/Desktop/p2p-lab/P2P-Project
# Start each client
for client in "${CLIENTS[@]}"; do
  read -r NODE_IP NODE_PORT NODE_NAME SERVE_PATH <<< "$client"
  echo "Starting client $NODE_NAME on port $NODE_PORT serves: $SERVE_PATH"
  start_client "$NODE_IP" "$NODE_PORT" "$NODE_NAME" "$SERVE_PATH"
done

echo "All clients started."
