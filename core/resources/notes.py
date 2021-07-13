from flask_restful import Resource
from core import mongo_db
from core.util import constants


class Notes(Resource):
    def get(self):
        docs = []
        for note in mongo_db.find():
            note['_id'] = str(note['_id'])
            docs.append(note)
        return docs, constants.OK
