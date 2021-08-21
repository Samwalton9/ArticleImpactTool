from yaml import safe_load

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, validators

app = Flask(__name__)

with open('secrets.yml', 'r') as secrets_file:
    secrets = safe_load(secrets_file)

app.config['SECRET_KEY'] = secrets['secret_key']


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        language = request.form.get('language')
        article_title = request.form.get('title')
        query_string = f"?lang={language}&title={article_title}"
        return redirect(url_for('results_page') + query_string)
    else:
        return render_template('homepage.html')


@app.route('/result', methods=['GET', 'POST'])
def results_page():
    language = request.args.get('lang')
    title = request.args.get('title')
    return render_template('result.html', language=language, title=title)


if __name__ == '__main__':
    app.run()
