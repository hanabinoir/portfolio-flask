import logging
import sys

from flask import Flask
from flask_restful import Api

import config
from routes import mongo, BasicInfo, Auth
from models import sa

app = Flask(__name__)
# config
app.config.from_object(config.Config)

# logger
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# mongo
mongo.init_app(app)
# sql
sa.init_app(app)

api = Api(app)
# resources
api.add_resource(BasicInfo, '/basic')
api.add_resource(Auth, '/user')

if __name__ == '__main__':
    app.run()
