# Hosts File Auto-Updater
This repository contains a Python script designed to automatically update the hosts file on Windows systems. The script fetches a list of hosts from a remote server and updates the local hosts file accordingly. This ensures that the latest host configurations are applied without manual intervention.
This tool is ideal for users looking to automate the management of their hosts file, ensuring it stays up-to-date with minimal effort.

## Key Features

- Automated Fetching: Retrieves the latest hosts list from a configurable remote URL.
- Logging: Detailed logs are maintained to track update history and any errors encountered during execution.

## Dependencies

- Python libraries: requests

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the script using `python hosts_updater.py`.

## Configuration

The script can be configured using the `config.json` file. This file contains the following fields:

- `hosts_url`: The URL from which the hosts list will be fetched.
- `hosts_path`: The path to the local hosts file on the system.
- `update_interval`: The frequency at which the hosts file will be updated (in seconds).
- `log_path`: The path to the log file where update history and errors will be recorded.

## Usage

1. Update the `config.json` file with the appropriate values.
2. Run the script using `python main.py`.
3. The script will periodically fetch the hosts list from the remote URL and update the local hosts file.

## Contributions

Contributions are welcome! For feature requests, bug reports or submitting pull requests, please use the [issue tracker](