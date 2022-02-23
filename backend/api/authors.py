from flask import Blueprint, current_app, json, request, Flask
from flask_cors import CORS, cross_origin 
# @cross_origins have been added in an attempt to solve CORS error, can remove if NGINX is successful
from api.models import Author, Paper, Tag
author_routes = Blueprint('author_routes', __name__, template_folder='templates')

# Routes starting with /api/authors

@author_routes.route('/authors', methods=['GET'])
def get_authors():
    return current_app.response_class(
        response=json.dumps([author.to_dict() for author in current_app.session.query(Author).all()]),
        status=200,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = current_app.session.query(Author).get(id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    return current_app.response_class(
        response=json.dumps(author.to_dict()),
        status=200,
        mimetype='application/json'
    )
        

@author_routes.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author = Author(data['name'])
    current_app.session.add(author)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps(author.to_dict()),
        status=201,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
    data = request.get_json()
    author = current_app.session.query(Author).get(id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'Author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if 'name' in data:
        author.name = data['name']
    if 'institution' in data:
        author.institution = data['institution']

    current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'author updated',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )
        

@author_routes.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = current_app.session.query(Author).get(id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    current_app.session.delete(author)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'author deleted',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )
        

@author_routes.route('/authors/<int:author_id>/papers/<int:paper_id>', methods=['PUT'])
def add_paper_to_author(author_id, paper_id):
    author = current_app.session.query(Author).get(author_id)
    paper = current_app.session.query(Paper).get(paper_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
    if not paper:
        return current_app.response_class(
            response=json.dumps({'message': 'paper not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    author.papers.append(paper)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'paper added to author',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:author_id>/papers/<int:paper_id>', methods=['DELETE'])
def remove_paper_from_author(author_id, paper_id):
    author = current_app.session.query(Author).get(author_id)
    paper = current_app.session.query(Paper).get(paper_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
    if not paper:
        return current_app.response_class(
            response=json.dumps({'message': 'paper not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    author.papers.remove(paper)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'paper removed from author',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:author_id>/papers', methods=['GET'])
def get_papers_by_author(author_id):
    author = current_app.session.query(Author).get(author_id)
    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
    return current_app.response_class(
        response=json.dumps([paper.to_dict() for paper in author.papers]),
        status=200,
        mimetype='application/json'
    )

# Tag list routes

@author_routes.route('/authors/<int:author_id>/tags', methods=['GET'])
def get_tags_by_author(author_id):
    author = current_app.session.query(Author).get(author_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
        
    return current_app.response_class(
        response=json.dumps([tag.to_dict() for tag in author.tags]),
        status=200,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:author_id>/tags/<int:tag_id>', methods=['PUT'])
def add_tag_to_author(author_id, tag_id):
    author = current_app.session.query(Author).get(author_id)
    tag = current_app.session.query(Tag).get(tag_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if tag not in author.tags:
        author.tags.append(tag)
        current_app.session.commit()
    
    return current_app.response_class(
        response=json.dumps({'message': 'tag added to author',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@author_routes.route('/authors/<int:author_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_author(author_id, tag_id):
    author = current_app.session.query(Author).get(author_id)
    tag = current_app.session.query(Tag).get(tag_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if tag in author.tags:
        author.tags.remove(tag)
        current_app.session.commit()
    
    return current_app.response_class(
        response=json.dumps({'message': 'tag removed from author',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )