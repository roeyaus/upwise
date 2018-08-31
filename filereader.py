import os, sys
from os.path import join
from config import ENCODING


class ReadFile:
    def __init__(self, filename):
        file_path = os.path.dirname(os.path.abspath(__file__))
        self.full_path = join(file_path, filename)

    @property
    def user_list(self):
        try:
            users_lists = []
            if os.path.exists(self.full_path):
                with open(self.full_path, "r", encoding=ENCODING) as file:
                    for line in file:
                        user_name = line.strip('\t\n\r\s')
                        if len(user_name) > 1:
                            users_lists.append(user_name)
                return users_lists
            else:
                raise Exception(f'Warning file named ({filename}) is missing')
        except Exception as e:
            sys.stderr.write(e)

