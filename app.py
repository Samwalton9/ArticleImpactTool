from helpers import construct_query_string
from modules.wikipedia import get_article_data, get_linked_pages, get_content_translated_pages
from modules.twitter import get_recent_tweets

import urllib.parse
from yaml import safe_load

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

with open('secrets.yml', 'r') as secrets_file:
    secrets = safe_load(secrets_file)

app.config['SECRET_KEY'] = secrets['secret_key']


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if request.form.get('language') and request.form.get('title'):
            query_string = construct_query_string(request.form)
            return redirect(url_for('results_page') + query_string)
        else:
            return render_template('homepage.html')
    else:
        return render_template('homepage.html')


@app.route('/result', methods=['GET', 'POST'])
def results_page():
    if request.method == 'POST':
        if request.form.get('language') and request.form.get('title'):
            query_string = construct_query_string(request.form)
            return redirect(url_for('results_page') + query_string)
        else:
            redirect(url_for('homepage'))

    else:
        language = request.args.get('lang')
        title = request.args.get('title')

        article_data = get_article_data(language, title)
        if "missing" in article_data:
            # Page doesn't exist, redirect to homepage.
            return redirect(url_for('homepage'))

        if 'thumbnail' in article_data:
            thumbnail_source = article_data['thumbnail']['source']
            url_list = thumbnail_source.split('/')[:-1]
            url_list.remove('thumb')
            full_size_source = '/'.join(url_list)
            page_image_url = full_size_source
        else:
            page_image_url = None
        # TODO: Fix when page_image_free is present but it's a local file. Check it resolves?

        context = {'language': language,
                   'title': article_data['title'],
                   'wikidata_id': article_data['pageprops']['wikibase_item'],
                   'page_image_url': page_image_url,
                   'page_created': article_data['revisions'][0]['timestamp'],
                   'creator': article_data['revisions'][0]['user'],
                   'page_url': f'{language}.wikipedia.org/wiki/{urllib.parse.quote(title)}'
                   }

        linked_pages = get_linked_pages(context['wikidata_id'])
        linked_pages.pop(language + "wiki")  # Remove language entered by the user
        linked_pages.pop('commonswiki', None)  # Remove commonswiki if present
        context['num_linked_pages'] = len(linked_pages)

        return render_template('result.html', **context)


@app.route('/get_translations')
def get_translated_articles():
    wikidata_id = request.args.get('wikidata_id')
    linked_pages = get_linked_pages(wikidata_id)
    translated_articles = get_content_translated_pages(linked_pages)
    return translated_articles


@app.route('/get_tweets')
def get_tweets():
    url = request.args.get('url')
    return get_recent_tweets(url)


if __name__ == '__main__':
    app.run()
