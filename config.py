import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True

    MONGO_URI = f"mongodb+srv://{os.getenv('MONGO_USR')}:" \
                f"{os.getenv('MONGO_PWD')}@" \
                f"{os.getenv('MONGO_HOST')}/" \
                f"{os.getenv('MONGO_DB')}?" \
                'retryWrites=true&w=majority'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USR')}:" \
                              f"{os.getenv('MYSQL_PWD')}@" \
                              f"{os.getenv('MYSQL_HOST')}/" \
                              f"{os.getenv('MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
