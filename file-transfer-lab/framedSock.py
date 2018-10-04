import re
     
rbuf = b""                      # static receive buffer

def framedReceive(sock, fname, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL|re.MULTILINE) # look for colon
             if match:#if not match recieve additional 100 bytes
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr)#if correct match test to see if lenght obtained correctly
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                       elif msgLength == 0:
                            print("zero length file not store... exiting")
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:#complete message received open file and put there
                 fname = "1"+fname
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 with open(fname,'w+') as fhandle:
                      fhandle.write(payload.decode())
                 sock.close()
                 return
                 #return payload
         r = sock.recv(100)#receive 100 bytes
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))

def putFileSend(sock, fname, debug=0):#THIS IS TO SEND THE FILE TO THE SERVER along with name
     f = open(fname, 'rb')#open file to read in bytes
     print("Sending file")
     pl = f.read(1024)
     while (pl):#while data read 
          msg = str(len(pl)).encode() + b':' + pl#place length in front of message separated by ':'
          while len(msg):
               nsent = sock.send(msg)
               msg = msg[nsent:]
          pl = f.read(1024)
     f.close()
     print("File Sent")

