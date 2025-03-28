# Gelos80Sniff
Gelos80Sniff is a Python tool designed for network scanning and web enumeration. It identifies devices with open ports in a given IP range and performs directory discovery on web servers (port 80) using Gobuster.

This program was developed to run on Kali Linux, but should work fine on any other debian based distribution. Windows support is limited.

Features
IP Range Validation: Checks the connectivity of the target IP range.

Port Scanning: Scans TCP ports (1-1024) and lists open ports.

Web Enumeration: Runs Gobuster to find hidden directories on port 80.

Export Results: Option to save Gobuster output to a TXT file.

Requirements
Python 3.x

nmap Python library – Install with:
- pip install python-nmap

Gobuster – Make sure it is installed (e.g., on Linux: sudo apt-get install gobuster).

How to Use
Clone the repository:
- git clone https://github.com/reiyua/Gelos80Sniff.git

Run the script with administrator privileges:
- sudo python3 Gelos80Sniff.py

Follow the prompts:

Enter an IP range (e.g., 192.168.1.0/24).

Specify your Gobuster wordlist path (e.g., /usr/share/wordlists/common.txt).

Optionally save the Gobuster results to a specific directory.

Example Paths
Gobuster wordlist example: /usr/share/wordlists/common.txt

Disclaimer
This tool is intended for educational purposes and authorized network testing only. Unauthorized use may violate legal and ethical standards. Always get permission before scanning any network.
