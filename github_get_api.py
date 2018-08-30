from config import API_GITHUB_URL, TIMEOUT, FILE_NAME_GITHUB_USERS, MAX_WORKERS, GITHUB_USER_TOKEN
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from filereader import ReadFile
import urllib.request
from database import DataBase
import json


class GithubReader:
    def __init__(self):
        self.db = DataBase()

    def load_url(self, url, timeout):
        res = urllib.request.Request(url, headers={'Authorization': f'token {GITHUB_USER_TOKEN}'})
        with urllib.request.urlopen(res, timeout=timeout, ) as conn:
            return json.loads(conn.read())

    def __call__(self):
        self.set_users_repo()

    def set_users_repo(self):
        all_repos_data = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            user_list = ReadFile(FILE_NAME_GITHUB_USERS).user_list
            full_url_list = [f"{API_GITHUB_URL}{username}/repos" for username in user_list]
            if user_list:
                future_to_url = {executor.submit(self.load_url, url, TIMEOUT): url for url in full_url_list}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        sys.stderr.write('%r generated an exception: %s \n' % (url, exc))
                    else:
                        all_repos_data.append(data)
        list_repo_max_stars = self.search_repo_by_stars(all_repos_data)
        if list_repo_max_stars:
            self.write_db_list_repo(list_repo_max_stars)
        else:
            sys.stdout.write(f"users do not have repositories where the rating is greater than at least one star")

    def search_repo_by_stars(self, data):
        user_repo_list = []
        for user_repos in data:
            if isinstance(user_repos, list) and user_repos:
                max_star_repo = list(map(lambda x: int(x.get('stargazers_count', 0)), user_repos))
                if len(max_star_repo):
                    index_max = max_star_repo.index(max(max_star_repo))
                    repo = user_repos[index_max]
                    if repo:
                        user_repo_list.append(repo.get('html_url', '').split('/')[-1])
        return user_repo_list

    def write_db_list_repo(self, list_repo):
        try:
            res = self.db.write_repo_name(list_repo)
            sys.stdout.write('\n data successfully recorded' if res else 'failed to write data')
        except Exception as e:
            sys.stderr.write(e)
