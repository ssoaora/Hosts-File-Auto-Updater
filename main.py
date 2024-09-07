import logging
import requests
import difflib

URL = "https://a.dove.isdumb.one/list.txt"
HOSTS_PATH = r"C:\\Windows\\System32\\drivers\\etc\\hosts"

BEGIN_MARKER = "# BEGIN AUTO UPDATE"
END_MARKER = "# END AUTO UPDATE"

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
            return lines
    except IOError as e:
        logging.error(f"Error reading hosts file: {e}")
        return []


def update_hosts_file(new_lines):
    try:
        with open(HOSTS_PATH, 'r+', encoding='utf-8') as file:
            lines = file.read().splitlines()

            # 찾기: BEGIN_MARKER와 END_MARKER 사이의 기존 데이터
            begin_index = None
            end_index = None
            for i, line in enumerate(lines):
                if line.strip() == BEGIN_MARKER:
                    begin_index = i
                elif line.strip() == END_MARKER:
                    end_index = i
                    break

            # 새 데이터 준비: BEGIN_MARKER와 END_MARKER 사이의 내용을 업데이트
            if begin_index is not None and end_index is not None:
                updated_lines = lines[:begin_index + 1] + new_lines + lines[end_index:]
            else:
                # 기존에 주석이 없으면 새로 추가
                updated_lines = lines + [BEGIN_MARKER] + new_lines + [END_MARKER]

            # 파일 쓰기
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

    # 주석 사이의 데이터만 비교하기 위해 로컬 데이터에서 해당 영역 추출
    try:
        begin_index = local_data.index(BEGIN_MARKER)
        end_index = local_data.index(END_MARKER)
        local_data_in_update_block = local_data[begin_index + 1:end_index]
    except ValueError:
        local_data_in_update_block = []

    diff = list(difflib.unified_diff(local_data_in_update_block, remote_data, lineterm=''))
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
