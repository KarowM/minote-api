from flask import Flask
from flask_pymongo import MongoClient

mongo_db = MongoClient('mongo_uri')['minote']['notes']
app = Flask(__name__)