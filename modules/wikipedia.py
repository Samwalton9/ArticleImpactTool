import requests


def get_article_data(language, title):
    """
    For a language code (e.g. "de") and a page title, get basic page data from the MediaWiki
    API.
    Returns JSON.
    """
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


def get_linked_pages(qid):
    """
    For a particular QID string (e.g. "Q9322750"), return a dictionary of language-title pairs
    for the pages linked to this item.
    """
    s = requests.Session()

    base_url = "https://wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": qid,
        "format": "json"
    }

    result = s.get(url=base_url, params=params)
    data = result.json()

    return data['entities'][qid]['sitelinks']


def get_content_translated_pages(sitelinks):
    """
    Given a dictionary of language-title pairs from get_linked_pages,
    return a dictionary of projects where the page has the contenttranslation tag.
    """
    # TODO: Limit to pages created _after_ the searched page.
    translated_articles = {}
    for project in sitelinks:
        language = sitelinks[project]['site'][:-4]
        title = sitelinks[project]['title']

        article_data = get_article_data(language, title)
        tags = article_data['revisions'][0]['tags']
        if 'contenttranslation' in tags:
            translated_articles[language] = {
                'title': article_data['title'],
                'page_created': article_data['revisions'][0]['timestamp'],
                'creator': article_data['revisions'][0]['user']
            }

    return translated_articles
