import requests

import settings


STARRED_QUERY ='''
{{ 
  user(login: "{username}"){{
    repositories(
      first:1, 
      orderBy: {{
        direction: DESC,
        field: STARGAZERS
      }}
    ){{
      nodes {{
        name
      }}
    }}
  }}
}}
'''


class GitHubApi(object):
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.GITHUB_API_KEY}',
        }
        self.api_url = 'https://api.github.com/graphql'

    def request(self, query):
        r = requests.post(
            self.api_url,
            json={'query': query},
            headers=self.headers
        )

        r.raise_for_status()

        r_json = r.json()
        errors = r_json.get('errors')
        if errors:
            raise ValueError('GitHub API returned some errors:\n{}'.format('\n'.join(str(err) for err in errors)))

        return r_json

    def get_starred_repo(self, username):
        r_json = self.request(STARRED_QUERY.format(username=username))

        return r_json['data']['user']['repositories']['nodes'][0]['name']
