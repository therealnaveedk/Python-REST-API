from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# CRUD APIS: create, read, update, delete. thats what most rest apis are
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )

    # cuz we added store_id to the item model
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Item needs store id!"
    )

    @jwt_required()
    def get(self, name):
        # can place try/catch here
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'},404

    def post(self,name):

        if ItemModel.find_by_name(name):
            return {'message': "an item with name '{}' already exists".format(name)},400 # something wrong with request

        data = Item.parser.parse_args()

        #item = ItemModel(name, data['price'], data['store_id'])
        # same as above, simplified it
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"mesage": "An error occurred inserting the item"}, 500 # server done messed up

        # always have to return json
        return item.json(), 201

    # Deleting the Item
    def delete(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        # does item exist
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        # since this item is uniquely identified by its id, SQLAlchemy will
        # update if the price has changed or it will insert a new one if it
        # did not exist
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    # all returns all the objects in the database
    def get(self):
        # remember x.json() is function that will be applied to each element and then make it into a list, thats how lambdas work
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, using lambdas
        return {'items': [item.json() for item in ItemModel.query.all()]} # using list comprehension
