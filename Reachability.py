import csv
import subprocess
import concurrent.futures
import os
from tqdm import tqdm

def ping_ip(ip_address):
    try:
        # Run ping command and capture the output
        result = subprocess.run(['ping','-c', '4','-w','5',ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        # Check if ping was successful
        if result.returncode == 0:
            return ip_address, "Reachable"
        else:
            return ip_address, "Not Reachable"
    except Exception as e:
        return ip_address, f"Error: {str(e)}"

def main():
    # Open the CSV file for reading
    with open('ips.csv', 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader, None)  # Read the header row, if it exists
        ips = [row[0] for row in csv_reader]  # Extract IP addresses from the CSV

    # Use ThreadPoolExecutor to ping multiple IPs concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=350) as executor:
        # Submit ping tasks for each IP
        ping_tasks = {executor.submit(ping_ip, ip): ip for ip in ips}

        # Collect ping results
        results = []
        with tqdm(total=len(ping_tasks)) as pbar:
            for future in concurrent.futures.as_completed(ping_tasks):
                ip = ping_tasks[future]
                try:
                    ip_address, result = future.result()
                    results.append((ip_address, result))
                except Exception as e:
                    print(f'Error pinging {ip}: {e}')
                pbar.update(1)  # Update progress bar

    # Write the results back to a temporary CSV file
    with open('ips_temp.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        # Write header if it existed
        if header:
            csv_writer.writerow(header)
        # Write results
        csv_writer.writerows(results)

    # Replace the original CSV file with the temporary one
    os.replace('ips_temp.csv', 'ips.csv')

if __name__ == "__main__":
    main()
