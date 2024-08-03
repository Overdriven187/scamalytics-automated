import os
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import Fore, Style, init

# Configuration
api_user = "username"
api_key = "apikey"
check_interval = 1  # Time between checks (in seconds)
max_workers = 10  # Number of threads

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(filename="ip_monitor.log", level=logging.INFO)

def get_fraud_score(ip):
    try:
        url = f"https://api11.scamalytics.com/{api_user}/?key={api_key}&ip={ip}"
        response = requests.get(url)
        response.raise_for_status()
        return ip, response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching fraud score for IP {ip}: {e}")
        return ip, None

def process_ip(ip, stats):
    ip = ip.strip()
    if ip:
        ip, fraud_score_data = get_fraud_score(ip)
        if fraud_score_data:
            score = fraud_score_data.get('score', 'unknown')
            risk = fraud_score_data.get('risk', 'unknown')
            stats['total'] += 1
            if score != 'unknown':
                if score >= 50:
                    stats['red'] += 1
                    folder = "Over_50"
                elif score >= 20:
                    stats['orange'] += 1
                    folder = "Over_20"
                else:
                    stats['green'] += 1
                    folder = "Below_20"

                # Write the IP address to the appropriate folder
                base_folder = "fraud_scores"
                os.makedirs(os.path.join(base_folder, folder), exist_ok=True)
                file_name = f"{base_folder}/{folder}/fraud_score_{score}.txt"
                with open(file_name, 'a') as output_file:
                    output_file.write(f"{ip}\n")

            # Log the processed IP
            logging.info(f"Processed IP {ip}: Fraud Score: {score}, Risk: {risk}")

def process_ips(file_path):
    stats = {'total': 0, 'red': 0, 'orange': 0, 'green': 0}

    try:
        with open(file_path, 'r') as file:
            ips = file.readlines()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_ip, ip, stats) for ip in ips]
            with tqdm(total=len(ips), desc="Checking IPs", bar_format="{l_bar}{bar}{r_bar}", dynamic_ncols=True) as pbar:
                for future in as_completed(futures):
                    future.result()  # Wait for each future to complete
                    pbar.update(1)
                    bar = '=' * (pbar.n * 20 // pbar.total)
                    percentage = (pbar.n / pbar.total) * 100
                    summary = f"{Fore.RED}Over 50: {stats['red']}{Style.RESET_ALL} | " \
                              f"{Fore.YELLOW}Over 20: {stats['orange']}{Style.RESET_ALL} | " \
                              f"{Fore.GREEN}Below 20: {stats['green']}{Style.RESET_ALL} "
                    pbar.set_postfix_str(f"Checking IPs: [{bar:<20}] {percentage:.2f}% {summary}")

    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = 'ips.txt'  # The file containing the list of IP addresses
    process_ips(input_file)
