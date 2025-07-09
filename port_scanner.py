import socket
import subprocess
import threading
from queue import Queue
import platform
import sys

# ====== Configuration ======
TARGET_HOST = input("Enter target IP or hostname (default: localhost): ").strip() or "127.0.0.1"
START_PORT = int(input("Enter start port (default: 1): ") or 1)
END_PORT = int(input("Enter end port (default: 1024): ") or 1024)
THREAD_COUNT = 100
OUTPUT_FILE = "scan_results.txt"
ENABLE_UDP_SCAN = input("Enable UDP scan? (y/N): ").lower() == 'y'

# ====== Shared Resources ======
port_queue = Queue()
open_ports = []
lock = threading.Lock()

# ====== System Info Function ======
def get_system_info():
    print("\n📋 Gathering system info...\n")
    try:
        if sys.platform.startswith("win"):
            result = subprocess.run(['systeminfo'], capture_output=True, text=True)
        else:
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
        print(result.stdout.strip())
    except Exception as e:
        print(f"Error gathering system info: {e}")

# ====== TCP Port Scanning ======
def scan_tcp_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((TARGET_HOST, port))
        if result == 0:
            try:
                sock.send(b"Hello\r\n")
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner"
            with lock:
                print(f"✅ Port {port}/TCP is OPEN — {banner}")
                open_ports.append((port, "TCP", banner))
        sock.close()
    except Exception:
        pass

# ====== UDP Port Scanning ======
def scan_udp_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b"Ping", (TARGET_HOST, port))
        try:
            data, _ = sock.recvfrom(1024)
            with lock:
                print(f"✅ Port {port}/UDP is OPEN — {data.decode(errors='ignore').strip()}")
                open_ports.append((port, "UDP", data.decode(errors='ignore')))
        except socket.timeout:
            pass  # Could be open|filtered
        sock.close()
    except Exception:
        pass

# ====== Thread Worker ======
def worker(protocol):
    while not port_queue.empty():
        port = port_queue.get()
        if protocol == "TCP":
            scan_tcp_port(port)
        elif protocol == "UDP":
            scan_udp_port(port)
        port_queue.task_done()

# ====== Start Scanning ======
def start_scan(protocol="TCP"):
    print(f"\n🔍 Scanning {TARGET_HOST} ports {START_PORT}-{END_PORT} over {protocol}...\n")
    for port in range(START_PORT, END_PORT + 1):
        port_queue.put(port)

    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=worker, args=(protocol,))
        t.daemon = True
        t.start()
        threads.append(t)

    port_queue.join()

# ====== Save to File ======
def save_results():
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Scan results for {TARGET_HOST}\n")
        f.write(f"Open ports:\n")
        for port, proto, banner in sorted(open_ports):
            f.write(f"{port}/{proto} — {banner}\n")
    print(f"\n📁 Results saved to {OUTPUT_FILE}")

# ====== Main Entry ======
if __name__ == "__main__":
    get_system_info()
    start_scan(protocol="TCP")
    if ENABLE_UDP_SCAN:
        start_scan(protocol="UDP")
    save_results()