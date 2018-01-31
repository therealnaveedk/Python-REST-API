# this is replicating the if statement that was present at the bottom of app.py
from app import app
from db import db

db.init_app(app)

# Also moved this block of code. now when we run this file this decorator gets created
# and has access to the db variable
# Flask decorator used to run this method before the the first request
# and this will create data.db and tables in the file that we defined up
# unless they already exist
# SQLAlchemy does this for us, no need to manually create tables anymore
@app.before_first_request
def create_tables():
    db.create_all()
