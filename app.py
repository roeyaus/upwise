from client import Client
from db import DB


if __name__ == '__main__':
    db = DB()
    client = Client()
    popular_repositories = client.process_file('users.txt')
    for user, repository in popular_repositories.items():
        db.add_user(user, repository['name'])
