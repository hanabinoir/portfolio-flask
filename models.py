import re
import uuid

from email_validator import validate_email, EmailNotValidError
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import or_
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

sa = SQLAlchemy()


class User(sa.Model):
    __tablename__ = 'user'
    id = sa.Column(sa.String, primary_key=True)
    email = sa.Column(sa.String(50), index=True, unique=True, nullable=False)
    username = sa.Column(sa.String(50), index=True, unique=True, nullable=False)
    password_hash = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now())

    def __init__(self, username, email):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email

    def create(self, pwd):
        self.set_password(pwd)
        sa.session.add(self)
        sa.session.commit()

    @classmethod
    def find(cls, username, email):
        res = cls.query.filter(
                or_(
                    User.username == username,
                    User.email == email
                )
            ).first()
        return res

    def set_password(self, pwd):
        if not pwd:
            raise AssertionError('Password not provided')

        if not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})', pwd):
            raise AssertionError('Password is not strong enough')

        if len(pwd) > 50:
            raise AssertionError('Password is too long')

        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('Username not provided')

        if self.query.filter(self.username == username).first():
            raise AssertionError('Username already exists')

        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 to 20 characters')

        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('Email not provided')

        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise AssertionError(str(e))


class Role(sa.Model):
    __tablename__ = 'roles'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(25), nullable=False)


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = auto_field()
    username = auto_field()


class RoleSchema(SQLAlchemySchema):
    class Meta:
        model = Role

    id = auto_field()
    name = auto_field()
