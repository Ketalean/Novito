from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('seller', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('contacts', required=True)
parser.add_argument('address', required=True)
parser.add_argument('stock', type=bool)
parser.add_argument('img', required=True)
parser.add_argument('category', required=True)
