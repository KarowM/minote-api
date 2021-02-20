from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

notes = [
    {
        'id': 0,
        'title': 'First note',
        'body': 'Body of first note'
    },
    {
        'id': 1,
        'title': 'Second note',
        'body': 'Body of second note'
    }
]


class Notes(Resource):
    def get(self):
        return notes


api.add_resource(Notes, '/api/notes', endpoint='all-notes')

if __name__ == "__main__":
    app.run()
