from peewee import *

from .core import BaseModel


class GithubRepo(BaseModel):
    repo_name = CharField(unique=True, column_name='Repo_name')

    class Meta:
        table_name='github_repo'
