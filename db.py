import sqlite3


DEFAULT_DB = 'sqlite.db'


class DB:
    def __init__(self, database=None):
        self.database = database or DEFAULT_DB
        self.conn = sqlite3.connect(self.database)
        self.add_table()

    def add_table(self):
        c = self.conn.cursor()
        c.execute('create table if not exists user '
                  '(id integer primary key, user text, repo text);')
        c.execute('delete from user;')

    def add_user(self, username, repo_name):
        c = self.conn.cursor()
        c.execute(
            'insert into user (user, repo) values (?, ?);',
            (username, repo_name)
        )
        self.conn.commit()
