# Hosts File Auto-Updater
This repository contains a Python script designed to automatically update the hosts file on Windows systems. The script fetches a list of hosts from a remote server and updates the local hosts file accordingly. This ensures that the latest host configurations are applied without manual intervention.
This tool is ideal for users looking to automate the management of their hosts file, ensuring it stays up-to-date with minimal effort.

## Key Features

- Automated Fetching: Retrieves the latest hosts list from a configurable remote URL.
- Logging: Detailed logs are maintained to track update history and any errors encountered during execution.

## Dependencies

- Python libraries: `requests`

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Update the `main.py` file with the appropriate values.
4. Run the script using `update.bat` or type `python main.py` on terminal (Note: Administrator privileges are required).
5. The script will fetch the hosts list from the remote URL and update the local hosts file.

## Configuration

The script can be configured editing functions. This file contains the following fields:

- `URL`: The URL from which the hosts list will be fetched.
- `HOSTS_PATH`: The path to the local hosts file on the system.

## Contributions

Contributions are welcome! For feature requests, bug reports or submitting pull requests, please use the issue tracker