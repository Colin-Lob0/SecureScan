import socket
import concurrent.futures
from urllib.parse import urlparse
from tqdm import tqdm

def extract_hostname(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.split(':')[0]  # Extracting hostname and removing port if present
        return hostname
    except Exception as e:
        print(f"Error extracting hostname: {e}")
        return None

def scan_port(hostname, port, open_ports, progress_bar):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    # Attempt to connect to the port
    result = sock.connect_ex((hostname, port))
    if result == 0:
        print(f"Port {port} is open")
        open_ports.append(port)
    sock.close()

    # Update the progress bar
    progress_bar.update(1)

def scan_ports(url, ports, open_ports, progress_bar):
    hostname = extract_hostname(url)

    if not hostname:
        print("Invalid URL. Please provide a valid URL.")
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map each port to the scan_port function
        executor.map(lambda port: scan_port(hostname, port, open_ports, progress_bar), ports)

def split_ports(num_threads, all_ports):
    ports_per_thread = len(all_ports) // num_threads
    thread_ports = [all_ports[i:i + ports_per_thread] for i in range(0, len(all_ports), ports_per_thread)]
    return thread_ports

def main():
    # Take URL input from the user
    target_url = input("Copy and paste the URL from the browser: ")

    # Resolve the IP address of the extracted hostname
    try:
        ip_address = socket.gethostbyname(extract_hostname(target_url))
    except socket.gaierror:
        print("Couldn't resolve the hostname.")
        return

    print(f"Scanning ports for {extract_hostname(target_url)} ({ip_address}):")

    # Define the range of ports to scan (all 65535 ports)
    all_ports = list(range(1, 65536))

    # Define the number of threads
    num_threads = 11

    # Initialize the progress bar
    with tqdm(total=len(all_ports), desc="Scanning Progress", unit="port", position=0, miniters=1) as progress_bar:
        # Split the ports among threads
        thread_ports = split_ports(num_threads, all_ports)

        # List to store open ports
        open_ports = []

        # Use ThreadPoolExecutor for concurrent port scanning
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit each thread's task to the executor
            for thread_id, ports in enumerate(thread_ports):
                executor.submit(scan_ports, target_url, ports, open_ports, progress_bar)

        # Display the list of open ports
        print("\nOpen Ports:", open_ports)

if __name__ == "__main__":
    main()
