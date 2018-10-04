#! /usr/bin/env python3

# Echo client program
import socket, os, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import putFileSend


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),#50001
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"#default is "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

fname = input("please enter name of file to send to server: ")
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f == fname:
        break
else:
    print("file for sending not found exiting")
    sys.exit(0)

print("sending file")
putFileSend(s, fname, debug)
