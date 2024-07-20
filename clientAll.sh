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
  local NODE_PORT=$2
  local NODE_NAME=$3
  local SERVE_PATH=$4
  local NODE_IP=$1
  gnome-terminal -- bash -c "python3 src/ClientApp.py $BOOTSTRAP_IP $BOOTSTRAP_PORT $NODE_IP $NODE_PORT $NODE_NAME $SERVE_PATH; exec bash"
}

# Start each client
for client in "${CLIENTS[@]}"; do
  read -r NODE_PORT NODE_NAME FILE_PATH <<< "$client"
  echo "Starting client $NODE_NAME on port $NODE_PORT serves: $FILE_PATH"
  start_client "$NODE_PORT" "$NODE_NAME" "$FILE_PATH"
done

echo "All clients started."
