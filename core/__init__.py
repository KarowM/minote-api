import os

import certifi
from flask import Flask
from flask_cors import CORS
from flask_pymongo import MongoClient
from flask_restful import Api

mongo_db = MongoClient(os.environ.get('mongo_uri'), ssl_ca_certs=certifi.where())['minote']['notes']
app = Flask(__name__)
CORS(app)
api = Api(app)
