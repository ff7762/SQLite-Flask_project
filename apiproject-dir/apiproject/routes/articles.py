from flask import abort, jsonify, request

from apiproject.baseapp import app
from apiproject.connector import db_session_wrap
from apiproject.models.article import Article
from apiproject.models.region import Region
from apiproject.models.author import Author

@db_session_wrap
def add_regions_to_article(article, region_ids, session):
    region_query = session.query(
        Region,
    ).filter(
        Region.id.in_(region_ids),
    )
    regions = region_query.all()
    if len(region_ids) != len(regions):
        raise Exception('One or more regions don\'t exist')

    article.regions = regions

@db_session_wrap
def add_authors_to_article(article, author_ids, session):
    author_query = session.query(
        Author,
    ).filter(
        Author.id.in_(author_ids),
    )
    authors = author_query.all()
    if len(author_ids) != len(authors):
        raise Exception('One or more authors don\'t exist')

    article.authors = authors

@app.route('/articles', methods=['GET'])
@db_session_wrap
def get_articles(session):
    query = session.query(
        Article
    ).order_by(
        Article.id
    )
    return_list = []
    for article in query:
        columns = article.asdict(follow=['regions', 'authors'])
        return_list.append(columns)

    return jsonify(return_list)

@app.route('/articles', methods=['POST'])
@db_session_wrap
def create_article(session):
    request_data = request.get_json()
    article = Article.fromdict(Article(), request_data)
    session.add(article)
    session.flush()
    if 'regions' in request_data:
        add_regions_to_article(
            article, [x['id'] for x in request_data['regions']],
            session=session,
        )

    if 'authors' in request_data:
        add_authors_to_article(
            article, [x['id'] for x in request_data['authors']],
            session=session,
        )

    return jsonify(article.asdict(follow=['regions', 'authors']))


@app.route('/articles/<int:article_id>', methods=['GET'])
@db_session_wrap
def get_article_route(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    return jsonify(articles[0].asdict(follow=['regions']))


@app.route('/articles/<int:article_id>', methods=['PUT'])
@db_session_wrap
def update_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    article = articles[0]

    request_data = request.get_json()
    article.fromdict(request_data)
    if 'regions' in request_data:
        add_regions_to_article(
            article,
            [x['id'] for x in request_data['regions']],
            session=session
        )

    if 'authors' in request_data:
        add_authors_to_article(
            article,
            [x['id'] for x in request_data['authors']],
            session=session
        )

    return jsonify(article.asdict(follow=['regions', 'authors']))


@app.route('/articles/<int:article_id>', methods=['DELETE'])
@db_session_wrap
def delete_article(article_id, session):
    query = session.query(
        Article
    ).filter(
        Article.id == article_id
    ).order_by(
        Article.id
    )
    articles = query.all()
    if not articles:
        abort(404)

    article = articles[0]

    session.delete(article)

    return jsonify(article.asdict(follow=['regions']))
