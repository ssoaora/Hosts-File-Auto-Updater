import logging
import requests
import difflib

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
            lines = file.read().splitlines()
            return lines[30:]  # Return lines starting from line 31
    except IOError as e:
        logging.error(f"Error reading hosts file: {e}")
        return []

def update_hosts_file(new_lines):
    try:
        with open(HOSTS_PATH, 'r+', encoding='utf-8') as file:
            lines = file.read().splitlines()
            original_lines = lines[:30]  # Keep the first 30 lines unchanged
            updated_lines = original_lines + new_lines
            file.seek(0)
            file.write('\n'.join(updated_lines) + '\n')
            file.truncate()
    except IOError as e:
        logging.error(f"Error updating hosts file: {e}")

def main():
    remote_data = fetch_remote_data()
    local_data = read_hosts_file()

    if not remote_data:
        logging.info("No remote data fetched. Exiting.")
        print("No remote data fetched. Exiting.")
        return

    diff = list(difflib.unified_diff(local_data, remote_data, lineterm=''))
    added_lines = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    removed_lines = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    modified_lines = added_lines + removed_lines

    if diff:
        logging.info("Differences found. Updating hosts file.")
        logging.info(f"Added lines: {added_lines}, Removed lines: {removed_lines}, Modified lines: {modified_lines}")
        update_hosts_file(remote_data)
        print(f"Differences found. Updating hosts file.")
        print(f"Added lines: {added_lines}, Removed lines: {removed_lines}, Modified lines: {modified_lines}")
    else:
        logging.info("No differences found. Hosts file is up to date.")
        print("No differences found.")
        print("Hosts file is up to date.")

    input("Press any key to exit...")

if __name__ == "__main__":
    main()