import logging
import os

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class BasicInfo(Resource):
    logging.basicConfig(filename='mongo.log', encoding='utf-8', level=logging.DEBUG)
    MONGO_USR = os.getenv("MONGO_USR")
    MONGO_PWD = os.getenv("MONGO_PWD")
    MONGO_DB = os.getenv("MONGO_DB")
    uri = f'mongodb+srv://{MONGO_USR}:{MONGO_PWD}@hanabitube.f7jyw.mongodb.net/{MONGO_DB}?' \
          f'retryWrites=true&w=majority'

    app.config["MONGO_URI"] = uri
    mongo = PyMongo(app)

    def get(self):
        b = self.mongo.db.basic.find_one()
        if b:
            b.pop('_id')
            return jsonify(b)
        return {'msg': 'The requested object does not exist.'}, 404

    def get(self, test):
        if test == 1:
            logging.debug(self.uri)
        return {'msg': 'Please check the log file'}


api.add_resource(BasicInfo,
                 '/basic', '/basic/<int:test>')


if __name__ == '__main__':
    app.run(debug=True, port=33507)
