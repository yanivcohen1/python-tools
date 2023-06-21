#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
import traceback

host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

while True:
    try:
        s = socket.socket() # Create a socket object
        s.connect((host, port))
        a = input("Enter the msg:")
        s.send(bytes(a, 'ascii'))
        recv = s.recv(1024)
        print("client rcv: ", str(recv.decode()))
        s.close()
    except Exception as ex :
        print("error desc: ", ex)
        traceback.print_exc()
        try:
            s.close()
        except:
            pass
