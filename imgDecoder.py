import os
import sys
import cv2
import socket, select
import numpy
import binascii
import json
import base64
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


def trim(data, delim):
    data_parsed = data.partition(delim)[0]
    return data_parsed

def recv_decode():
    
    data_decode = ''
    print(">>Packet Receieved, Decoding...")
    while True:
        data_decode += (base64.b64decode(conn.recv(BUFFER_SIZE))).decode()
        if '<END>' in data_decode:
            print(data_decode)
            if("<CMD>") in data_decode:
                print(">>Command Packet Received")
                break
            elif("<DATA>") in data_decode:
                print(">>Data Packet Received")
                break
            else:
                print("Malformed Command")
                break
    return data_decode

def getpic(data):
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
        decd = recv_decode()
        #data_decode = base64.b64decode(data)
        print(decd)
        #data_foo = Struct.unpack('hh', data_decode)

        
except KeyboardInterrupt:
    conn.close()
    sock.close()