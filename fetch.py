import threading

import settings
from github_api import GitHubApi


def get_starred_repo(user):
    github = GitHubApi()

    try:
        print(github.get_starred_repo(user))
    except Exception as e:
        print(e)

if __name__ == '__main__':


    threads = []
    with open(settings.USERS_FILE) as users:
        for user in users:
            user = user.replace('\n', '').strip()
            threads.append(threading.Thread(target=get_starred_repo, args=(user,)))

    for t in threads:
        t.start()


