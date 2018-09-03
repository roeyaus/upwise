import threading

import settings
from database.models import GithubRepo
from github_api import GitHubApi


def get_starred_repo(user):
    github = GitHubApi()

    try:
        repo = github.get_starred_repo(user)
        GithubRepo.create(repo_name=repo)
        print(repo)
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


