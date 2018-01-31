# Instead of storing stuff in an in memory db we have now stored them on a sqlite
# db that can be retrieved

# contains an in memory table of all our registered users
# pretend this is a db
# if we had many users then the username_mapping and userid_mapping
# would grow accordingly

# from the user file we import the User class
# this workzeug is for older python versions and it does safe string comp
# from workzeug.security import safe_str_cmp
from models.user import UserModel

# function used to authenticate the user
# given username and password, function will select the correct username
# from our list
# When the user authenticates, i.e sends in the auth endpoint with a username
# and password, we pass those 2 in, retrieve user object using the mapping and
# compare the user's password to the mappings password
# if they match, we return the user and then that gets used to generate the
# JWT
def authenticate(username, password):
    user = UserModel.find_by_username(username)

    # for older versions latter part of if would be (using workzeug)
    # safe_str_cmp(user.password,password)
    if user and user.password == password:
        return user

# this function is unique to Flask-JWT
# takes in a payload and payliad is the contents of the JWT token
# whenever a user requests an endpoint where they need to be authenticated,
# this identity method is used
# so we get a payload coming from the request and in that payload, we get the
# identity, which is the user id and there we retrieve the user object using the
# id mapping and if it matches, the JWT was correct and user knows he is logged
# in
def identity(payload):

    # extract user id from the payload
    user_id = payload['identity']

    # retreive user that matches this payload
    return UserModel.find_by_id(user_id)
