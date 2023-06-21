#!/usr/bin/python           # This is server.py file
import socket  # Import socket module
import traceback
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # for tcp
# s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # for udp

host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

# only for TCP mode not need for udp
s.listen(5)  # Now wait for client connection.

# A forever loop until we interrupt it or
# an error occurs
while True:
    try:
        # Establish connection with client.
        c, addr = s.accept()
        # print recv msg
        msg = str(c.recv(1024).decode())
        print("server recv : ", msg)
        # send echo msg
        c.sendall(bytes(msg, "ascii"))
        # for udp echo
        # c.sendto(bytes(msg, "ascii"), addr)

        # Close the connection with this client
        c.close()
    except Exception as ex :
        print("error desc: ", ex)
        traceback.print_exc()
        try:
            c.close()
        except:
            pass
