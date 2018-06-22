import os
import sys
import cv2
import socket, select
import numpy
import binascii
import json
from struct import *

HOST_STR = ''
PORT = 10000
BUFFER_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_addr = (HOST_STR, PORT)
sock.bind(('', 10000))
print(">> Starting server at " , sock.getsockname())
sock.listen(1)
print(">> Waiting for connection at " , sock.getsockname())
conn, client_addr = sock.accept()
print('>> Client connected at ', client_addr)


def decode(data):
    picture = data.partition("#$#$#$")[0]
    msg = data.partition("#$#$#$")[2]
    print(msg)
    print('>> parsed img')
    b = binascii.a2b_base64(picture)
    nparr = numpy.fromstring(b, dtype=numpy.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print('>> encoded img')
    # try:
    #     cv2.imshow('asdf', frame)
    #     cv2.waitKey(0)
    # except:
    #     print('error')
    # cv2.destroyAllWindows()
    return frame
    

def sendResp(resp):
    conn.send(resp.encode())
    print('>> Sent Test Msg:' + resp)
    return

resp = ''
try:
    while True:
        #data = conn.recv(BUFFER_SIZE)
        data = conn.recv(BUFFER_SIZE)
        resp += data.decode()
        print(resp)
        # if "#$#$#$" in data:
        #     frame = decode(data)   
        serverResp = "<RESP>"
        sendResp(serverResp)
        
except KeyboardInterrupt:
    conn.close()
    sock.close()