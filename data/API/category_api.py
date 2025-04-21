from flask import Flask, jsonify
from flask_restful import abort, Api, Resource

from data import db_session

from data.categories import Category
from .category_parser import parser

app = Flask(__name__)
api = Api(app)


class CategorysResource(Resource):
    def get(self, category_id):
        abort_if_user_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        return jsonify({'category': category.to_dict(
            only=('id', 'name'))})

    def delete(self, category_id):
        abort_if_user_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})


class CategorysListResource(Resource):
    def get(self):
        session = db_session.create_session()
        category = session.query(Category).all()
        return jsonify({'category': [item.to_dict(
            only=('id', 'name')) for item in category]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(
            name=args['name']
        )
        session.add(category)
        session.commit()
        return jsonify({'id': category.id})


def abort_if_user_not_found(category_id):
    try:
        category_id = int(category_id)
    except Exception:
        abort(400, message=f"Value Error: Category id is not int")
    session = db_session.create_session()
    category = session.query(Category).get(category_id)
    if not category:
        abort(404, message=f"Category {category_id} not found")
