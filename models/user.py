import sqlite3
from db import db

# This is an API, not a REST one. It exposes 2 methods that are used internally, it is an interface for us internally
# As long as we dont change the API, we dont worry about its affects. security file uses it and we changed implementation
# of the API but as long as our api returns the ame thing, its all good

# In the same vein, we have our endpoints and web/mobile app interacting with those endpoints doesnt care if its written in
# python or ruby, all it cares about is that its getting the data back that it requested in the expected format


class UserModel(db.Model):
    #telling SQLAlchemy the table name where these models are going to be stored
    __tablename__ = 'users'

    # what columns we want the table to contain
    # this is how SQLAlchemy reads these items
    # when it looks at this columns it will pass them in the __init__ method
    # below and create an object for each row in our db
    # id is a builtin python method but using it like this here is ok cuz we are not using
    # it anywhere else
    # can use uuid universally unique identifier long string of numbers, chars and dashes and is
    # universally unique in the app if we want to add our own id
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80)) # max 80 chars
    password = db.Column(db.String(80))

    #_ id is being used cuz id is a python keyword
    # we got rid of it cuz its a primary key which means it is auto incrementing and its automatically assigned and
    # so when we create the object through SQLAlchemy the self.id is given to us as well
    # hence we dont need to create it
    def __init__(self,username, password):
        # these have to match the above.
        # if we have something extra here, it wont affect the db, just wont be
        # stored
        # removed this since it is automatically (read comment above method)
        # self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first() # first item returned and then converted to a UserModel object

   # mapping for userid
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()# id is column name in db, _id is the argument we passed in
