import os

USERS_FILE = 'users.txt'

GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')


try:
    from local_settings import *
except ImportError:
    pass
