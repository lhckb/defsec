import subprocess
import platform
import threading
from queue import Queue
import os

def ping_ip(ip, results_queue):
    """
    Ping the specified IP address and store the result in a queue.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]

    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        results_queue.put(ip)
        print(f"{ip} is active.")
    except subprocess.CalledProcessError:
        print(f"{ip} is inactive.")

def worker(ip_queue, results_queue):
    """
    Thread worker function to ping IPs from the queue.
    """
    while not ip_queue.empty():
        ip = ip_queue.get()
        ping_ip(ip, results_queue)
        ip_queue.task_done()

def scan_lan_multithreaded():
    """
    Scan all IP addresses in the 192.168.1.x range using multiple threads and write responsive IPs to a text file.
    """
    ip_queue = Queue()
    results_queue = Queue()
    base_ip = "192.168.1."
    
    # Enqueue all IP addresses
    for i in range(256):
        ip_queue.put(base_ip + str(i))
    
    # Get the number of threads to use
    num_threads = os.cpu_count()  # Maximum number of threads based on CPU cores

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip_queue, results_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    ip_queue.join()

    # Collect results from the queue
    active_ips = []
    while not results_queue.empty():
        active_ips.append(results_queue.get())

    # Write active IPs to a text file
    with open("ex01_active_ips.txt", "w") as f:
        for ip in active_ips:
            f.write(ip + "\n")

    print(f"Active IPs have been written to 'active_ips.txt'.")

if __name__ == "__main__":
    scan_lan_multithreaded()
