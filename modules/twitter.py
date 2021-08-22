import requests
from yaml import safe_load

with open('secrets.yml', 'r') as secrets_file:
    secrets = safe_load(secrets_file)

bearer_token = secrets['twitter_bearer_token']

search_url = "https://api.twitter.com/2/tweets/search/recent"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython-WikipediaArticleImpactTool"
    return r


def get_recent_tweets(url):
    params = {'query': f'{url}'}
    response = requests.request("GET",
                                search_url,
                                auth=bearer_oauth,
                                params=params)
    return response.json()
