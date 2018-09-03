import settings
from github_api import GitHubApi


if __name__ == '__main__':
    github = GitHubApi()

    with open(settings.USERS_FILE) as users:
        for user in users:
            user = user.replace('\n', '').strip()

            try:
                print(github.get_starred_repo(user))
            except Exception as e:
                print(e)

