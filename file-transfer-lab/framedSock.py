import re
     
rbuf = b""                      # static receive buffer

def framedReceive(sock, fname, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL|re.MULTILINE) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                       elif msgLength == 0:
                            print("zero length file not store... exiting")
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 fname = "1"+fname
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 with open(fname,'w+') as fhandle:
                      fhandle.write(payload.decode())
                 sock.close()
                 return
                 #return payload
         r = sock.recv(100)
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))

def putFileSend(sock, fname, debug=0):#THIS IS TO SEND THE FILE TO THE SERVER along with name
     f = open(fname, 'rb')
     print("Sending file")
     pl = f.read(1024)
     while (pl):
          msg = str(len(pl)).encode() + b':' + pl
          while len(msg):
               nsent = sock.send(msg)
               msg = msg[nsent:]
          pl = f.read(1024)
     f.close()
     print("File Sent")

