from peewee import *


db = MySQLDatabase(
    host='52.255.62.8',
    user='test_user',
    password='test_user',
    database='test'
)

class BaseModel(Model):
    class Meta:
        database = db

