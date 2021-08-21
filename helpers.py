def construct_query_string(form_data):
    language = form_data.get('language')
    article_title = form_data.get('title')
    return f"?lang={language}&title={article_title}"