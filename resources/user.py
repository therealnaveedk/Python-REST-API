import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# a resrouce so we can add it to the api
# could create flask endpoint too, dont matter
# good thing is we only need to do post now
class UserRegister(Resource):

    # remember parser will parse through json request and make sure username
    # password are there
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type = str, # 12.00 shows up and not 12
        required = True, # no request comes thru without a price
        help = "This field cannot be left blank!"
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be left blank!"
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # below is the same as this: user = UserModel(data['username'], data['password'])
        # this is a dictionary with 2 keys and each has its own values so we can unpack it
        # it says: for each of the keys in data, username = its value, password = its value
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
