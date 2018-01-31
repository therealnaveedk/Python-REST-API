# Create an item model
# Internal representation of an item
# So we moved stuff from item.py in resources to here
from db import db

# db.Model tells SQLAlchemy that this class here is a thing that we will be saving
# and retrieving to a db. hence it will create a mapping between the objects and
# the db
class ItemModel(db.Model):

    __tablename__ = 'items'

    # having an id for an entity is useful
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) # 2 decimal places

    # added a new Column and has to be an Integer cuz it has to match the
    # store's id type in store.py
    # stores is the name of the table in store.py and id is the column name
    # Foreignkey allows us to find all the items in a store due to the store id
    # of an item matching the id of a store
    # hence they are linked, which is due to Foreignkey
    # store.id in items is a foreign key cuz it has values identical to the id
    # (which is a primary key) of another table in store.py
    # hence if you have items in a store, you cant delete this store, cuz they have Foreignkey references
    # so you would have to either delete items, move them or change their store
    # ids.
    # so there is some security and control.
    # so now we can ask hey what store do we belong to
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # (we can also do this with a join in sql.
    # will see it later but we dont have to use joins cuz SQLAlchemy does it for us)
    # sees we have a store id, and therefore we can find a store in the db that matches this store id
    # every ItemModel has a property store , that is the store that matches this store id
    # we can do a back reference and that is in the store.py
    store = db.relationship('StoreModel')

    # adding store_id
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    #returns JSON representation of a model, basically a dictionary
    def json(self):
        return {'name': self.name, 'price': self.price}

    # returns an object of type model as opposed to a dictionary
    # cls is a reference to the class remember
    @classmethod
    def find_by_name(cls, name):
        # .query is not something we defined, it is a query builder that comes
        # from db.Model from SQLAlchemy
        # we dont have to do any connection etc. it does it automatically
        # filter_by is also a query builder like .query
        # so we even do ItemModel.query.filter_by(name=name, id=1)
        # returns 1st row only and it is an ItemModel object
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    # the ItemModel represents an item, so we can use self.
    # SQLAlchemy will do an update automatically instead of an insert due to the fact that
    # it knows the unique id. so we consolidate insert and update into one method
    # called upserting
    def save_to_db(self):
            # SQLAlchemy can directly translate from object to row in a db
            # so we dont have to tell it what row data to insert
            # we just have to tell it to insert the object in the db
            # object we are currently dealing with is self

            # session: in this instance is a collection of objects we will write
            # to the db
            # can add multiple objects to a session and then write them all at
            # once and thats more efficient
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
