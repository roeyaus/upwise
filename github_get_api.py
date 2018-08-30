from config import API_GITHUB_URL, TIMEOUT, FILE_NAME_GITHUB_USERS, MAX_WORKERS
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from filereader import ReadFile
import urllib.request
from database import DataBase


class GithubReader:
    def __init__(self):
        self.db = DataBase()

    def load_url(self, url, timeout):
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return conn.read()

    @property
    def get_users_repo(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            user_list = ReadFile(FILE_NAME_GITHUB_USERS).user_list
            full_url_list = [f"{API_GITHUB_URL}{username}" for username in user_list]
            if user_list:
                future_to_url = {executor.submit(self.load_url, url, TIMEOUT): url for url in full_url_list}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        sys.stderr.write('%r generated an exception: %s' % (url, exc))
                    else:
                        print(data)


