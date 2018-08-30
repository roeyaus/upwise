from mysql.connector import connect, Error
from config import USER, DATABASE_NAME, PASSWORD, HOST_DB, TABLE_NAME
import sys


class DataBase:
    connect = None

    def __init__(self):
        try:
            self.connect = connect(user=USER, password=PASSWORD, host=HOST_DB, database=DATABASE_NAME)
        except Error as e:
            self.connect = None
            self.cursor = None
            sys.stderr.write(e)
        else:
            if not self.__table_exist:
                self.__create_table()

    def write_repo_name(self, repo_name):
        try:
            if self.connect is not None:
                cur = self.connect.cursor(buffered=True)
                query = f"INSERT INTO {TABLE_NAME} (repo_name) VALUES(%s)"
                cur.execute(query, [repo_name])
                self.connect.commit()
                cur.close()
            else:
                raise Exception('there is no connection to the database')
        except Exception as e:
            sys.stderr.write(e)

    def __create_table(self):
        try:
            if self.connect is not None:
                cur = self.connect.cursor(buffered=True)
                query = f"CREATE TABLE {TABLE_NAME} (id serial PRIMARY KEY,repo_name VARCHAR(255) NOT NULL)"
                cur.execute(query)
                cur.close()
            else:
                raise Exception('there is no connection to the database')
        except Exception as e:
            sys.stderr.write(e)

    @property
    def __table_exist(self):
        try:
            if self.connect is not None:
                cur = self.connect.cursor(buffered=True)
                query = f"SHOW TABLES LIKE '%{TABLE_NAME}%'"
                cur.execute(query)
                res = cur.fetchone()
                cur.close()
                return res[0] in [TABLE_NAME] if len(res) else False
            else:
                raise Exception('there is no connection to the database')
        except Exception as e:
            sys.stderr.write(e)

