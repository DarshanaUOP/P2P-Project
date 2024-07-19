#!/bin/bash

# Define common parameters
BOOTSTRAP_IP="127.0.0.1"
BOOTSTRAP_PORT=5555
NODE_IP="127.0.0.1"

# Define unique parameters for each client
CLIENTS=(
  "6001 node1 ./FileSystem"
  "6002 node2 ./FileSystem2"
  "6003 node3 ./FileSystem"
  "6004 node4 ./FileSystem2"
)

# Function to start client in a new terminal
start_client() {
  local NODE_PORT=$1
  local NODE_NAME=$2
  local SERVE_PATH=$3
  gnome-terminal -- bash -c "python3 src/ClientApp.py $BOOTSTRAP_IP $BOOTSTRAP_PORT $NODE_IP $NODE_PORT $NODE_NAME $SERVE_PATH; exec bash"
}

# Start each client
for client in "${CLIENTS[@]}"; do
  read -r NODE_PORT NODE_NAME FILE_PATH <<< "$client"
  echo "Starting client $NODE_NAME on port $NODE_PORT serves: $FILE_PATH"
  start_client "$NODE_PORT" "$NODE_NAME" "$FILE_PATH"
done

echo "All clients started."
