from flask import jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, reqparse
from models import User, UserSchema

parser = reqparse.RequestParser()
parser.add_argument('lang', type=str, help='default: JP')

mongo = PyMongo()


class BasicInfo(Resource):
    def get(self):
        args = parser.parse_args(strict=True)
        lang = args['lang']
        if lang:
            lang = lang.strip().upper()
        langs = ['EN', 'JP']
        if not lang or lang not in langs:
            b = mongo.db.basic.find_one({'lang': 'EN'})
        else:
            b = mongo.db.basic.find_one({'lang': lang})

        if b:
            b.pop('_id')
            return jsonify(b)
        return {'msg': 'The requested object does not exist.'}, 404


class Auth(Resource):
    def get(self):
        res = User.query.all()
        return jsonify(UserSchema().dump(res, many=True))
