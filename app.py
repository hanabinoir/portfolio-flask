import logging
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

import config
from auth import auth
from routes import mongo, Basic, Profile, Auth, Contact
from models import sa

app = Flask(__name__)
# config
app.config.from_object(config.Config)

CORS(app)

''' 
Temporary solution for Heroku environment 
'''
load_dotenv()
ON_CLOUD = os.getenv('CLOUD')
if ON_CLOUD:
    app.config['MONGO_URI'] = os.getenv('MONGO_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MYSQL_URL')

# logger
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# mongo
mongo.init_app(app)
# sql
sa.init_app(app)

api = Api(app)
# resources
api.add_resource(Basic, '/basic')
api.add_resource(Profile, '/profile')
api.add_resource(Contact, '/contact')
api.add_resource(Auth, '/user')
app.register_blueprint(auth)


@app.route('/test', methods=['GET'])
def test():
    return {
        'mysql': app.config['SQLALCHEMY_DATABASE_URI'],
        'mongo': app.config['MONGO_URI']
    }


if __name__ == '__main__':
    app.run()
