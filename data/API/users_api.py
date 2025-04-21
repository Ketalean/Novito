from flask import Flask, jsonify
from flask_restful import abort, Api, Resource

from data import db_session

from data.users import User
from .user_parser import parser

app = Flask(__name__)
api = Api(app)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'username', 'phone', 'address', 'reg_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'username', 'phone', 'address', 'reg_date')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            username=args['username'],
            phone=args['phone'],
            address=args['address'],
            reg_date=args['reg_date']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_user_not_found(user_id):
    try:
        user_id = int(user_id)
    except Exception:
        abort(400, message=f"Value Error: User id is not int")
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
