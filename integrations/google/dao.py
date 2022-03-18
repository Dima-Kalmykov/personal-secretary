from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from variables.env_variables import DATABASE_URL

# Database prefix for SqlAlchemy should starts with postgresql, not postgres
# (can't override this env variable in heroku)
# modified_db_url = DATABASE_URL

db_engine = create_engine(DATABASE_URL)
base = declarative_base()
Session = sessionmaker(db_engine)
session = Session()


def init_db_tables_if_needed():
    base.metadata.create_all(db_engine)


class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    google_token = Column(String)
    google_refresh_token = Column(String)
    email = Column(String)

    def __init__(self, user_id, token, refresh_token, email):
        self.id = user_id
        self.google_token = token
        self.google_refresh_token = refresh_token
        self.email = email


def get_user_by_id(user_id):
    return session.query(User).get(user_id)


def add_user(user):
    session.add(user)
    session.commit()


def delete_user(user_id):
    user = get_user_by_id(user_id)
    session.delete(user)
    session.commit()


def update_user(user_id, new_token, new_refresh_token, new_email):
    user = get_user_by_id(user_id)
    user.google_token = new_token
    user.google_refresh_token = new_refresh_token
    user.email = new_email
    session.commit()
