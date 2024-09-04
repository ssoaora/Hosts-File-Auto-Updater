import os
import sys

import pystray
import requests
import threading
import time
import logging
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import win32api
import win32com.client

URL = "https://a.dove.isdumb.one/list.txt"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
CHECK_INTERVAL = 3600  # 1 hour in seconds

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
            return file.read().splitlines()
    except IOError as e:
        logging.error(f"Error reading hosts file: {e}")
        return []

def append_to_hosts(missing_lines):
    try:
        with open(HOSTS_PATH, 'a') as file:
            for line in missing_lines:
                file.write(f"{line}\n")
        logging.info("Missing lines appended to hosts file.")
    except IOError as e:
        logging.error(f"Error writing to hosts file: {e}")

def check_and_update_hosts():
    remote_data = fetch_remote_data()
    if not remote_data:
        return

    local_data = read_hosts_file()
    missing_lines = [line for line in remote_data if line and line not in local_data]

    if missing_lines:
        append_to_hosts(missing_lines)

def run_periodically():
    while True:
        check_and_update_hosts()
        time.sleep(CHECK_INTERVAL)

def add_to_startup():
    script_path = os.path.realpath(sys.argv[0])
    startup_path = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup", "hosts_updater.lnk")

    if not os.path.exists(startup_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(startup_path)
        shortcut.TargetPath = script_path
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.Save()
        logging.info("Added to startup.")

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill="black")
    return image

def on_quit(icon):
    icon.stop()
    win32api.PostQuitMessage(0)

def setup_tray_icon():
    icon = pystray.Icon("hosts_updater", create_image(), "Hosts Updater", menu=pystray.Menu(
        item('Quit', on_quit)
    ))
    icon.run()

if __name__ == "__main__":
    add_to_startup()

    tray_thread = threading.Thread(target=setup_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    run_periodically()