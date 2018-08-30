import concurrent.futures
import json
from urllib import request as r
from urllib import error

class Scrap:
    def __init__(self, users ):
        self.token = '35c8a7d29f0ca3dc60d2a5256d639381d74cf27f'
        self.github_url_user = 'https://api.github.com/users/{0}'
        self.github_url_repos = 'https://api.github.com/users/{0}/repos?per_page={1}'
        self.users = users
        self.result = {}

    def _add_to_db(self, name):
        pass

    def process(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            future_usernames = {e.submit(self._scrap, username): username for username in self.users}
            for future in concurrent.futures.as_completed(future_usernames):
                res = future_usernames[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (res, exc))
                else:
                    self.result[res] = data


    def _scrap(self, username):
        try:
            req_user = r.Request(self.github_url_user.format(username))
            req_user.add_header('Authorization', 'token '+self.token)
            res = r.urlopen(req_user)
        except error.HTTPError:
            return 'Unable to fetch username'

        user_info = json.loads(res.read())

        req_repos = r.Request(self.github_url_repos.format(username, user_info['public_repos']))
        req_repos.add_header('Authorization', 'token ' + self.token)
        res_repos = r.urlopen(req_repos)
        user_repos = json.loads(res_repos.read())
        max_stars = max(d['stargazers_count'] for d in user_repos)
        max_repo = [repo for repo in user_repos if repo['stargazers_count'] == max_stars]

        return max_repo['name']




f = open('users.txt','r')
users = [x.strip() for x in f.readlines()]
scr = Scrap(users)
scr.process()