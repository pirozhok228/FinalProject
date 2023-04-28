import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Marks(SqlAlchemyBase, UserMixin):
    __tablename__ = 'marks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_email = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.email"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    math = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    russian = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chemistry = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phisics = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    biology = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    history = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    geografy = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    english = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User')
