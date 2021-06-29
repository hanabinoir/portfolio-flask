from flask import jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, reqparse
from models import User, UserSchema

parser = reqparse.RequestParser()
parser.add_argument('lang', type=str, help='default: JP')

mongo = PyMongo()


def search_by_collection(collection):
    args = parser.parse_args(strict=True)
    lang = args['lang']
    if lang:
        lang = lang.strip().upper()
    langs = ['EN', 'JP']
    if not lang or lang not in langs:
        res = mongo.db[collection].find_one({'lang': 'EN'})
    else:
        res = mongo.db[collection].find_one({'lang': lang})

    return res


def make_result(res):
    if res:
        res.pop('_id')
        return jsonify(res)
    return {'msg': 'The requested object does not exist.'}, 404


class Basic(Resource):
    def get(self):
        res = search_by_collection('basic')
        return make_result(res)


class Profile(Resource):
    def get(self):
        res = search_by_collection('profile')
        return make_result(res)


class Contact(Resource):
    def get(self):
        res = search_by_collection('contact')
        return make_result(res)


class Auth(Resource):
    def get(self):
        res = User.query.all()
        return jsonify(UserSchema().dump(res, many=True))
