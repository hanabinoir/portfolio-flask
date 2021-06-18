import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True

    MONGO_URI = 'mongodb+srv://{usr}:{pwd}@{host}/{db}?' \
                'retryWrites=true&w=majority'\
        .format(**{
            'usr': os.getenv('MONGO_USR'),
            'pwd': os.getenv('MONGO_PWD'),
            'host': os.getenv('MONGO_HOST'),
            'db': os.getenv('MONGO_DB'),
        })

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usr}:{pwd}@{host}/{db}'\
        .format(**{
            'usr': os.getenv('MYSQL_USR'),
            'pwd': os.getenv('MYSQL_PWD'),
            'host': os.getenv('MYSQL_HOST'),
            'db': os.getenv('MYSQL_DB'),
        })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
