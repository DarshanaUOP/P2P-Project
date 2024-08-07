Read Me

## Please note that we are using base 64 encoding to send file names and paths to avoid space issues

Project Structure
-----------------

| (root) contain Simple one click run shell scripts (clientAll.sh, server.sh)
|
|-- (src)  Folder contain all project source codes (ClientApp.py and Server.py) 



1) Libraries
____________
This project uses python request library. that need to be installed. it can be done by installing it from requirements.txt or from pip

Run: pip3 install requests

2) Start Bootstrap Server
_________________________
    Method 1: run ./server.sh 
    Method 2: run python3 src/ServerApp.py 

3) Start Clients
________________
    Method 1: run python3 src/ClientApp.py $BOOTSTRAP_IP $BOOTSTRAP_PORT $NODE_IP $NODE_PORT $NODE_NAME $SERVE_PATH (use relevant values replacing $VALUE)
    Method 2: 
        i. First you have to generate some random files to serve. use random file generator to do that 
            run ./genarateDirs.sh 4 (this generate 4 directories with random content)
        ii. run ./clientAll.sh (this start 4 clients serving above directories)

4) Usage
_________
    1) The Client contain simple CLI to operate. Following command can be used
        help                - List all the commands
        search <stuff>      - Search files on nodes
        download <hash>     - Download file (Hash is a unique hash created with file content, which is different even the file names are same and content are different)
        ls l                - List All Files from serving Directory
        ls r                - List ALl Files from remote files that searched (this contain hash and file name and node info)
        leave               - Leave the system
        reset               - Re join to the system (this changes connected nodes and bootstrap server give randomly picked 2 nodes)
        peers               - list connected peers (Nodes) 