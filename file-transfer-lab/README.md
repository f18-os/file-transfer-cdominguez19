## Description

This lab was meant for us to learn TCP file transfering between client and
server, learn the basics of sockets, and proxys. All of these elements were
meant to be combined in order to establish a connection and be able to
transfer a file and handle multiple clients(os.fork()).


## Code

The code is separated into multiple files. fileClient.py handles the client
side of the tcp connection, encoding the file that is to be sent and making
sure the file exists. The fileServer.py file simply receives the file(using a
modified version of Professor Freudenthal fileSend def). The framedSock.py
defines the crucial methods that both the client and server file use.

## How to Run

To run program...

```
1. C-x 2 (to split screen horizontally)
2. create 2 shells. One named client and one named server (M-x rename-buffer)
3. python3 fileServer.py on the server shell
4. python3 fileClient.py on the client shell
5. follow prompt
6. All this can also be ran along with the stammer proxy simply open another
shell for stammerProxy.py(run using python3 stammmerProxy.py)
To terminate simply C-x C-c
```

## Bugs
I was not able to handle the scenario in which I have to check the server to
see if the file already exists there. I was also not able to implement
handling the connection between host and client getting dissconected. Other
than that, the program seems to run correctly.
