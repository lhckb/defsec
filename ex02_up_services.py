import socket
import threading
from queue import Queue
import os

# Define target host
target_host = "192.168.1.1"  # Replace with the target IP or hostname
port_range = (1, 1024)      # Range of ports to scan

# Queue to hold port numbers to scan
port_queue = Queue()
# List to store open ports
open_ports = []

def scan_port(port):
    """
    Scan a specific port to check if it's open.
    """
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        # Try to connect to the port
        result = sock.connect_ex((target_host, port))
        if result == 0:
            print(f"Port {port} is open.")
            open_ports.append(port)
        sock.close()
    except socket.error as e:
        print(f"Error scanning port {port}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def worker():
    """
    Thread worker function to process ports from the queue.
    """
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(port)
        port_queue.task_done()

def main():
    """
    Main function to perform the port scan.
    """
    # Enqueue all ports in the specified range
    for port in range(port_range[0], port_range[1] + 1):
        port_queue.put(port)
    
    # Determine the number of threads to use (based on CPU count)
    num_threads = os.cpu_count()  # You can adjust this number depending on your machine's capabilities

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    port_queue.join()

    # Write open ports to a text file
    with open("ex02_open_ports.txt", "w") as f:
        f.write(f"Target Host: {target_host}\n")
        for port in open_ports:
            f.write(f"{port}\n")

    print(f"Scanning complete. Open ports have been written to 'ex02_open_ports.txt'.")

if __name__ == "__main__":
    main()
