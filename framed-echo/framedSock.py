import re

def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]
     
rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
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
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 with open('test.txt','w+') as fhandle:
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
     #fname = input("Enter file name to send to server: ")
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
     #sock.shutdown(sock.SHUT_WR)#Not sure on this part
     #sock.close()

#WHAT IS NEEDED IS A WAY TO RECIVE THE FILE SERVERSIDE AND STORE IT
def getFileSend(sock, debug = 0):
     f = open('test.txt','w+')
     global rbuf
     state = "getLength"
     msgLength = -1
     while True:
          print("inside loop")
          if (state == "getLength"):#if size not arrived yet then recv another 100 bytes of data
               match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL|re.MULTILINE) # look for colon
               print("inside getLength")
               if match:
                    lengthStr, rbuf = match.groups()
                    try:
                         msgLength = int(lengthStr)
                    except:
                         if len(rbuf):
                              print("badly formed message length:", lengthStr)
                              return None
                    state = "getPayload"
          if state == "getPayload":#if payload not size stated then receive another 100 bytes of data
               print("inside getPayload")
               if len(rbuf) >= msgLength:
                    payload = rbuf[0:msgLength]
                    rbuf = rbuf[msgLength:]
                    #return payload instead of returning collected msg, put into file
                    print("here")
                    npayload = payload.decode()
                    f.write(npayload)
          r = sock.recv(100)
          rbuf += r
          if len(r) == 0:
               if len(rbuf) != 0:
                    print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
                    return None
          if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
