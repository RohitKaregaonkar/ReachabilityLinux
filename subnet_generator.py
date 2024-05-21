import ipaddress
import csv

def generate_ips_to_csv(subnet, output_file):
    try:
        subnet_obj = ipaddress.IPv4Network(subnet)
        ips = [str(ip) for ip in subnet_obj.hosts()]

        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP Address'])
            for ip in ips:
                writer.writerow([ip])

        print(f"IP addresses written to {output_file}")
    except ValueError as e:
        print("Error:", e)

# Example usage:
subnet_id = "172.16.0.0/16" # Change this to your desired subnet ID
output_file = "./ips.csv"  # Change this to the desired output file path
generate_ips_to_csv(subnet_id, output_file)
