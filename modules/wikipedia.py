import requests


def get_article_data(language, title):
    s = requests.Session()

    base_url = f'https://{language}.wikipedia.org/w/api.php'
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageprops|revisions",
        "format": "json",
        "rvprop": "timestamp|user|comment|tags",
        "rvlimit": "1",
        "rvdir": "newer"
    }

    result = s.get(url=base_url, params=params)
    data = result.json()

    pages = data['query']['pages']
    for page in pages:
        return pages[page]  # There should only be one page, we just don't know the ID.
