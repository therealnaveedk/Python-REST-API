# Create a store model
# Internal representation of a store
from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    # having an id for an entity is useful
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    #back reference does the opposite
    # allows a store to see which items are in the items database with a store id
    # equal to its own id
    # this is saying we have a relationship with ItemModel, and then SQLAlchemy says
    # okay there is a relationship there. whats the relationship?
    # it goes into the item model and finds the store id there and says
    # "aha there is a store id in the item, which means that 1 item is related to a store.
    # and thus there could be more than 1 item related to the same store"
    # hence it knwos the store variable in item.oy is a single store (only one store an item is related to)
    # but the items variable in the store.py (below) can be many items so therefore items is a list of
    # item models. (many to 1). can be many items with the same store id

    # Whenever we create a StoreModel, this relationship is also created
    # meaning, if we have many stores and we have many items, whenever we create a StoreModel
    # we are going to go and create an object for each item in the db that matches that store id
    # now if we have a few items that is fine, but alot can be expensive
    # so to avoid that, that we can tell SQLAlchemy to not to that i.e. do not go into the items
    # table and create an object for each item YET.
    # we do that by lazy = 'dynamic'.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # returns JSON representation of a model, basically a dictionary
    # Because we used lazy = 'dynamic', we have to do self.items.all()
    # why? when we use lazy = 'dynamic', self.items is no longer a list of items
    # instead it is a query builder that has the ability to look into the items table
    # this means that until we call the json method, we are not looking into the table
    # which means creating stores is very simple
    # However it also that everytime we call the json method, we have to go in to the
    # table so then it will be slower that if we create a store, load up all the items and then call
    # the json method manytimes for free essentially.
    # so if we use lazy = 'dynamic', everytime we call the json method, we have to go into the table
    # so then that is slower. so there is a trade off there between the speed of creation of the store
    # and speed of calling the json method, thats upto you which to call
    # we stick with this in this case, cuz our StoreModel will get created when we want to access the data
    # (thats how we are doing it in the Store Resource)
    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
