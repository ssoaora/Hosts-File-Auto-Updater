import logging

import requests

URL = "https://a.dove.isdumb.one/list.txt"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

logging.basicConfig(filename='hosts_updater.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_remote_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching remote data: {e}")
        return []

def read_hosts_file():
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as file:
            lines =  file.read().splitlines()
            return lines[30:]  # Return lines starting from line 31
    except IOError as e:
        logging.error(f"Error reading hosts file: {e}")
        return []

def append_to_hosts(missing_lines):
    try:
        with open(HOSTS_PATH, 'a') as file:
            for line in missing_lines:
                file.write(f"{line}\n")
        logging.info(f"{len(missing_lines)} lines appended to hosts file.")
        return len(missing_lines)
    except IOError as e:
        logging.error(f"Error writing to hosts file: {e}")
        return 0

def check_and_update_hosts():
    remote_data = fetch_remote_data()
    if not remote_data:
        return 0, 0

    local_data = read_hosts_file()
    missing_lines = [line for line in remote_data if line and line not in local_data]
    removed_lines = [line for line in local_data if line and line not in remote_data]

    added_count = 0
    if missing_lines:
        added_count = append_to_hosts(missing_lines)
        logging.info(f"{added_count} lines added to hosts file.")
    else:
        logging.info("No updates found")

    if removed_lines:
        logging.info(f"{len(removed_lines)} lines removed from hosts file.")

    return added_count, len(removed_lines)

def run_once():
    added_count, removed_count = check_and_update_hosts()
    print("========================================")
    print(f"Update is finished.\n{added_count} lines added.\n{removed_count} lines removed.\nPress any key to exit.")
    input()

if __name__ == "__main__":
    run_once()