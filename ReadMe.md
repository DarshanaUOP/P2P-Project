## Install Required Libraries
`pip3 install requests`

### Note: We have tested this on linux environment and MAC OS
### You can use Client and Server shell script to start multiple applications
### Random Files can be generated from generate shell script
### Follow Instruction to Run the Program

## Start Server
Boostrap server runs on port 5555

![image](https://github.com/user-attachments/assets/6d919a41-c2b6-41fe-8e69-5d41d9cd0379)

```
 python3 Server.py 

```

## Start Client
```
python3 Client.py <ServerIp> <serverPort:5555>  <ClientIp> <ClientPort> <NameFortheClient> <sharedDirectory>
```

## Command

### Search Files
```
Command: search <some file name or part>
```
### List Files
```
Command: ls <path>
```
path:
- r - remote
- l - local

### Download Files
```
Command: download <hash>
```
### Neighbour Table
```
Command: peers
```
### Change Neibour
```
Command: reset
```
### Help
```
Command: help
```

### Leave
```
Command: leave
```
