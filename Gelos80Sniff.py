# © Rayyan Hodges, TAFE NSW, Gelos Enterprises, DataTrust 2025
# rayyan.hodges@studytafensw.edu.au
# This program is coded in Python and designed to scan the local network for any clients connected that have port 80 open.
# If a machine is found to have port 80 open, proceed to use programs like GoBuster and dirb to check for hidden directories without proper security in place and exploit.
# Results are exported to a TXT file for convenience.

# Import required python modules
import nmap
import subprocess
import os # integrate with operating system to make, manipulate and save the file.

# Function to validate user specified IP range and check IP address connectivity
def validate_ip_range(ip_range):
    print(f"Validating IP address range: {ip_range}")
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=ip_range, arguments='-sn')  # Ping scan to validate range
        if scanner.all_hosts():
            print("IP address range is valid and reachable.")
            return True
        else:
            print("No devices found. Please check the IP range.")
            return False
    except Exception as e:
        print(f"Error validating IP range: {e}")
        return False

# Function to perform the network scan and identify open ports
def perform_scan(ip_range):
    print(f"Starting network scan on {ip_range}...")
    scanner = nmap.PortScanner()
    scanner.scan(hosts=ip_range, arguments='-p 1-1024')
    results = {}
    for host in scanner.all_hosts():
        open_ports = scanner[host]['tcp'].keys() if 'tcp' in scanner[host] else []
        if open_ports:
            results[host] = open_ports
            print(f"Open ports on {host}: {open_ports}")
    return results

# Function to run Gobuster if port 80 is open
def run_gobuster(ip):
    print(f"Running web enumeration on {ip} (port 80)...")
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
            choice = input("Do you want to save the Gobuster results? (yes/no): ").strip().lower()
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

