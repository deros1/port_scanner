 Advanced Python Port Scanner

A multithreaded, cross-platform port scanner built in Python. This tool is designed for ethical hacking, network auditing, and cybersecurity education. It performs fast TCP scans, optional UDP scans, banner grabbing, and system info collection — all from your terminal.


   FEATURES

• Multithreaded TCP Port Scanning
• Optional UDP Scanning
•Remote Target Scanning
•Service Banner Grabbing (from open ports)
• OS Detection (uname -a or systeminfo)
•Saves Results to scan_results.txt
•Works on Windows, Linux, and macOS



Preview 

Enter target IP or hostname (default: localhost): 127.0.0.1
Enter start port (default: 1): 20
Enter end port (default: 100): 100
Enable UDP scan? (y/N): y

 Gathering system info...

Linux kali 6.3.0-5-amd64 #1 SMP Debian 6.3.13-1 ...

🔍 Scanning 127.0.0.1 ports 20-100 over TCP...

 Port 22/TCP is OPEN — SSH-2.0-OpenSSH_8.4p1
 Port 80/TCP is OPEN — HTTP/1.1 400 Bad Request

Results saved to scan_results.txt


---

Installation

> Python 3.x required

Clone this repository or download the script:
Run it:
python port_scanner.py

