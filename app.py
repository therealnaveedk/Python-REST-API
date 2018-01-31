# The item and itemlist were copy and pasted in the item.py and then stuff added to it
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# Note: when we import format file, ex: user, python runs the file. it looks at
# methods but does not run them but it can detect syntax errors
# However if the file has a statement, ex: print ("Hello"), everytime we import
# this file it runs all statements
#looks at resources package and then the item file
from resources.user import UserRegister
from resources.item import Item, ItemList

# when you do any import, SQLAlchemy goes to that file. so ex: it sees you imported Store.
# so it goes to the store in resources. there it sees you imported StoreModel from
# the models package and then goes there and there it sees the db. Hence if you hadnt included this
# the store tables would not be created
# in some casese if you dont have a resources associated to something you want to store in a db,
# just import the model directly
from resources.store import Store, StoreList

app = Flask(__name__)

# tell SQLAlchemy where data.db is located, in this case root of project.
# we can replace sqlite with MySQL, PostgreSQL, Oracle and SQLAlchemy will just
# work. literally just have to change this one like from sqlite to what you want
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# turns off Flask SQLAlchemy modification tracker
# does NOT turn off SQLAlchemy modification tracker
# changing extensions behaviour, not underlying behaviour
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'naveed'
api = Api(app)

#if you want to change the url authentication endpoint to /login instead of
# the default which is /auth, add the following before the creation of jwt instance.
# app.config['JWT_AUTH_URL_RULE'] = '/login' (and change /auth to /login in postman)

# config JWT to expire within half an hour. default is 5 minutes
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity)

# Sometimes we may want to include more information in the authentication response
# body, not just the access_token. For example, we may also want to include the
# user's ID in the response body. In this case, we can do something like this:
# remember to add from flask import jsonify
# now in postman you will see user id and access_token
# Remember that the identity should be what you've returned by the authenticate() function
# not recommended cuz security issues
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#                         'access_token': access_token.decode('utf-8'),
#                         'user_id': identity.id
#                    })
#


# By default, Flask-JWT raises JWTError when an error occurs within any of the
# handlers (e.g. during authentication, identity, or creating the response).
# In some cases we may want to customize what our Flask app does when such an
# error occurs. We can do it this way:
# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify({
#                        'message': error.description,
#                        'code': error.status_code
#                    }), error.status_code

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# The above means if we imported app.py, into say user.py, it would run this line
# and we dont want that. so we add this if statemen to combat it
# now when you a run a python file, python alwys aassigns a special name to that
# file and in this case it is __main__
# running app.py is main, if we run the user.py file then user.py is __main__
# hence the file you run is main
# if not main, it means we have imported it and hence we dont want to run the
# flask app
if __name__=='__main__':
    # we are importing here due to circular imports
    # our item models etc will import db as well, so if we import db at the top
    # and import the models at the top, when we import the model, model imports db
    # db will be in app and that creates a circular import
    # this code is executed when we directly execute app.py from python command line
    # python app.py and therefore this runs
    # however when we run this from uwsgi, uwsgi is loading the app variable above
    # app = Flask(__name__) and running it itself. IT IS NOT RUNNING THE app.py file
    # so therefore this never runs and nor does app.run but uwsgi runs the app for us
    # so issue is we are not importing db and hence it does not know it exists
    # the solution is to have another file (we called it run.py)
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
