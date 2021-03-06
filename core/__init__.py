from flask import Flask
from flask_pymongo import MongoClient
from flask_restful import Api

mongo_db = MongoClient('mongo_uri')['minote']['notes']
app = Flask(__name__)
api = Api(app)
