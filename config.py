import logging
import os

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
