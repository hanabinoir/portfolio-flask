from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

sa = SQLAlchemy()


class User(sa.Model):
    __tablename__ = 'user'
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String(50), index=True, unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.Date)
    updated_at = sa.Column(sa.Date)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    name = auto_field()
