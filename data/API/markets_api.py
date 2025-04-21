from flask import Flask, jsonify
from flask_restful import abort, Api, Resource

from data import db_session

from data.markets import Market
from .market_parser import parser

app = Flask(__name__)
api = Api(app)


class MarketsResource(Resource):
    def get(self, market_id):
        abort_if_user_not_found(market_id)
        session = db_session.create_session()
        user = session.query(Market).get(market_id)
        return jsonify({'market': user.to_dict(
            only=('id', 'title', 'description', 'seller', 'price', 'contacts',
                  'address', 'stock', 'category'))})

    def delete(self, market_id):
        abort_if_user_not_found(market_id)
        session = db_session.create_session()
        user = session.query(Market).get(market_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class MarketsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(Market).all()
        return jsonify({'market': [item.to_dict(
            only=('id', 'title', 'description', 'seller', 'price', 'contacts',
                  'address', 'stock', 'category')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        market = Market(
            title=args['title'],
            description=args['description'],
            seller=args['seller'],
            price=args['price'],
            contacts=args['contacts'],
            address=args['address'],
            stock=args['stock'],
            img=args['img'],
            category=args['category']
        )
        session.add(market)
        session.commit()
        return jsonify({'id': market.id})


def abort_if_user_not_found(market_id):
    try:
        market_id = int(market_id)
    except Exception:
        abort(400, message=f"Value Error: Market id is not int")
    session = db_session.create_session()
    market = session.query(Market).get(market_id)
    if not market:
        abort(404, message=f"Market {market_id} not found")
