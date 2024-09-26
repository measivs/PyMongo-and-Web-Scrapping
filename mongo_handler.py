from pymongo import MongoClient

class MongoHandler:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['recipe_database']
        self.collection = self.db['recipes']

    def insert_recipe(self, recipe_data):
        self.collection.insert_one(recipe_data)
