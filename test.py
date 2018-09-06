import unittest

from unittest import mock

import requests

from client import Client
from db import DB


responses = {
    'astropy': [
        {'name': 'astropy', 'stargazers_count': 1846},
        {'name': 'astropy-tutorials', 'stargazers_count': 75},
    ],
    'dimagi': [
        {'name': 'AadharUID', 'stargazers_count': 5},
        {'name': 'cloudcare-tests', 'stargazers_count': 0},
    ],
}


class MockResponse:
    def __init__(self, json_data, status_code, url):
        self.json_data = json_data
        self.status_code = status_code
        self.url = url

    def json(self):
        return self.json_data


def mocked_sessions_request(*args, **kwargs):
    url = args[1]

    username = Client.user_re.search(url).group(1)

    if username in responses:
        return MockResponse(responses[username], 200, url)

    return MockResponse(None, 404, url)


class ClientTestCase(unittest.TestCase):
    @mock.patch(
        'requests.sessions.Session.request',
        side_effect=mocked_sessions_request
    )
    def test_get_popular_repositories(self, mock_get):
        client = Client()
        popular_repositories = client.process_file('test_users.txt')
        self.assertEqual(popular_repositories['astropy']['name'], 'astropy')
        self.assertEqual(popular_repositories['dimagi']['name'], 'AadharUID')


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DB(':memory:')
    def test_add_user(self):
        self.db.add_user('james', 'musiccreator')
        c = self.db.conn.cursor()
        c.execute('select user, repo from user;')
        row = c.fetchone()
        self.assertEqual(row[0], 'james')
        self.assertEqual(row[1], 'musiccreator')


if __name__ == '__main__':
    unittest.main()
