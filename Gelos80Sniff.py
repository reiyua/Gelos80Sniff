# © Rayyan Hodges, TAFE NSW, Gelos Enterprises, DataTrust 2025
# rayyan.hodges@studytafensw.edu.au
# This program is coded in Python and designed to scan the local network for any clients connected that have port 80 open.
# If a machine is found to have port 80 open, it proceeds to use programs like GoBuster to check for hidden directories.
# Results are exported to a TXT file for convenience.

# Import required python modules
import nmap  # pip install python-nmap
import subprocess
import os  # Integrates with the OS for file operations
import signal

# Timeout Exception Handling
class TimeoutException(Exception):
    pass


def handler(signum, frame):
    raise TimeoutException("Nmap scan timed out!")


# Function to validate user-specified IP range and check IP address connectivity
def validate_ip_range(ip_range):
    print(f"Validating IP address range: {ip_range}")
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=ip_range, arguments='-sn')  # Ping scan to validate the range
        if scanner.all_hosts():
            print("IP address range is valid and reachable.")
            return True
        else:
            print("No devices found. Please check the IP range.")
            return False
    except Exception as e:
        print(f"Error validating IP range: {e}")
        return False


# Function to perform the network scan and echo results IP by IP
def perform_scan(ip_range):
    print(f"Starting network scan on {ip_range}...\n")
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=ip_range, arguments='-p 1-1024')
        results = {}

        for host in scanner.all_hosts():
            print(f"Scanning IP address: {host}")
            open_ports = scanner[host]['tcp'].keys() if 'tcp' in scanner[host] else []
            if open_ports:
                print(f"  --> Open ports on {host}: {list(open_ports)}")
                results[host] = open_ports
            else:
                print(f"  --> No open ports found on {host}.")

        return results

    except Exception as e:
        print(f"Error during network scan: {e}")
        return {}


# Function to run Gobuster if port 80 is open
def run_gobuster(ip):
    print(f"\nRunning web enumeration on {ip} (port 80)...")
    output_file = f"gobuster_results_{ip.replace('.', '_')}.txt"
    command = f"gobuster dir -u http://{ip} -w /path/to/wordlist.txt -o {output_file}"
    subprocess.run(command, shell=True)
    print(f"Enumeration complete. Results saved to {output_file}.")
    return output_file


# Main function to handle the process
def main():
    while True:
        ip_range = input("Enter the target IP address range (e.g., 192.168.1.0/24): ")
        if validate_ip_range(ip_range):
            break
        else:
            print("Invalid IP range or connectivity issue. Please try again.")

    # Perform network scan
    scan_results = perform_scan(ip_range)

    # Check scan results
    if not scan_results:
        print("No devices found with open ports. Exiting.")
        return

    # Check for open port 80 and run Gobuster
    for ip, ports in scan_results.items():
        if 80 in ports:
            output_file = run_gobuster(ip)

            # Offer to save results
            choice = input("\nDo you want to save the Gobuster results? (yes/no): ").strip().lower()
            if choice == "yes":
                save_path = input("Enter the directory to save the results: ")
                if os.path.isdir(save_path):
                    os.rename(output_file, os.path.join(save_path, output_file))
                    print(f"Results saved to {os.path.join(save_path, output_file)}")
                else:
                    print("Invalid directory. Results not saved.")
            else:
                print("Results not saved.")

    print("Process complete. Terminating.")


if __name__ == "__main__":
    main()
