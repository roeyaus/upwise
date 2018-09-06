import re

from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession


class Client:
    user_re = re.compile(r'users/(.*)/')

    def process_file(self, filename):
        users = []
        with open(filename, 'r') as f:
            for l in f:
                users.append(l.strip())

        urls = [self.get_user_repos_url(username) for username in users]

        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))

        futures = [session.get(url) for url in urls]

        popular_repositories = {}

        for f in futures:
            r = f.result()
            username = self.user_re.search(r.url).group(1)
            if r.status_code == 200:
                print('Found {}'.format(username))
                popular_repository = self.pick_popular_reposity(r.json())
                if popular_repository:
                    print(
                        'Found a popular repository {}'.format(
                            popular_repository['name']
                        )
                    )
                    popular_repositories[username] = popular_repository
                else:
                    print('User does not have any repositories')
            elif r.status_code == 404:
                print('Not found {}'.format(username))
            else:
                print('Could not fetch {} repos'.format(username))

        return popular_repositories

    def pick_popular_reposity(self, repos_list):
        if not repos_list:
            return False

        return max(repos_list, key=lambda x: x['stargazers_count'])

    def get_user_repos_url(self, username):
        return 'https://api.github.com/users/{}/repos'.format(username)
