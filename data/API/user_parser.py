import datetime

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('phone', required=True)
parser.add_argument('address', required=True)
parser.add_argument('password', required=True)
parser.add_argument('reg_date', default=datetime.datetime.now(), type=datetime)
