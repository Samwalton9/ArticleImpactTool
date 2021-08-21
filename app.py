from helpers import construct_query_string
from modules.wikipedia import get_article_data

from yaml import safe_load

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

with open('secrets.yml', 'r') as secrets_file:
    secrets = safe_load(secrets_file)

app.config['SECRET_KEY'] = secrets['secret_key']


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        query_string = construct_query_string(request.form)
        return redirect(url_for('results_page') + query_string)
    else:
        return render_template('homepage.html')


@app.route('/result', methods=['GET', 'POST'])
def results_page():
    if request.method == 'POST':
        query_string = construct_query_string(request.form)
        return redirect(url_for('results_page') + query_string)

    else:
        language = request.args.get('lang')
        title = request.args.get('title')

        article_data = get_article_data(language, title)

        if 'page_image_free' in article_data['pageprops']:
            page_image_url = "https://upload.wikimedia.org/wikipedia/commons/f/f3/" + article_data['pageprops']['page_image_free']
        else:
            page_image_url = None

        context = {'language': language,
                   'title': article_data['title'],
                   'wikidata_id': article_data['pageprops']['wikibase_item'],
                   'page_image_url': page_image_url,
                   'page_created': article_data['revisions'][0]['timestamp'],
                   'creator': article_data['revisions'][0]['user']
                   }

        return render_template('result.html', **context)


if __name__ == '__main__':
    app.run()
