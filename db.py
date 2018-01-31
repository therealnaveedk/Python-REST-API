from flask_sqlalchemy import SQLAlchemy

# links to our flask app and will look at all the objects we tell it to, and then it will map
# those objects to rows in a db
# saving an objects properties into a db - SQLAlchemy excels at this
db = SQLAlchemy()
