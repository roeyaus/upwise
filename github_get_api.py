from config import API_GITHUB_URL, TIMEOUT, FILE_NAME_GITHUB_USERS, MAX_WORKERS, GITHUB_USER_TOKEN, ASYNCIO_USE
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from filereader import ReadFile
import urllib.request
from database import DataBase
import json

if ASYNCIO_USE:
    import asyncio
    from asyncio import TimeoutError
    import aiohttp
    from aiohttp import ClientResponseError, ClientOSError


class GithubReader:
    '''
    some useful comments that describe purpose of class :)
    '''
    all_repos_data = []

    def __init__(self):
        self.db = DataBase()
        user_list = ReadFile(FILE_NAME_GITHUB_USERS).user_list
        self.full_url_list = [f"{API_GITHUB_URL}{username}/repos" for username in user_list]

    def load_url(self, url, timeout):
        '''
        nice comment that describe function work.
        :param url:
        :param timeout:
        :return:
        '''
        res = urllib.request.Request(url, headers={'Authorization': f'token {GITHUB_USER_TOKEN}'})
        with urllib.request.urlopen(res, timeout=timeout, ) as conn:
            return json.loads(conn.read())

    def __call__(self):
        self.set_user_by_repo_asincio() if ASYNCIO_USE else self.set_users_repo()

    def set_users_repo(self):
        '''
        comments
        :return:
        '''
        self.all_repos_data = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            if self.full_url_list:
                future_to_url = {executor.submit(self.load_url, url, TIMEOUT): url for url in self.full_url_list}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        sys.stderr.write('%r generated an exception: %s \n' % (url, exc))
                    else:
                        self.all_repos_data.append(data)
            self._write_data()

    async def fetch(self, session, url):
        '''
        async data fetch
        :param session:
        :param url:
        :return:
        '''
        try:
            async with session.get(url, timeout=TIMEOUT) as response:
                status = response.status
                if status == 200:
                    return await response.json()
                else:
                    sys.stderr.write('%r generated an exception: %s \n' % (url, status))
        except (ClientResponseError, ClientOSError, TimeoutError) as e:
            sys.stderr.write('%r generated an exception: %s \n' % (url, e))

    async def load_url_asinc(self, url):
        '''

        :param url:
        :return:
        '''
        try:
            async with aiohttp.ClientSession(headers={'Authorization': f'token {GITHUB_USER_TOKEN}'}) as session:
                data = await self.fetch(session, url)
                self.all_repos_data.append(data)
        except(ClientResponseError, ClientOSError, TimeoutError) as e:
            sys.stderr.write(e)

    def set_user_by_repo_asincio(self):
        '''
        function writer
        :return:
        '''
        self.all_repos_data = []
        ioloop = asyncio.get_event_loop()
        if self.full_url_list:
            tasks = [ioloop.create_task(self.load_url_asinc(url)) for url in self.full_url_list]
        ioloop.run_until_complete(asyncio.wait(tasks))
        ioloop.close()
        self._write_data()

    def _write_data(self):
        '''
        general db writer
        :return:
        '''
        if self.all_repos_data:
            list_repo_max_stars = self.search_repo_by_stars(self.all_repos_data)
            if list_repo_max_stars:
                self.write_db_list_repo(list_repo_max_stars)
            else:
                sys.stdout.write(f"users do not have repositories where the rating is greater than at least one star")

    def search_repo_by_stars(self, data):
        '''
        function for seearch max stars in repo
        :param data:
        :return:
        '''
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
