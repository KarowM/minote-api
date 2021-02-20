from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

notes = {
    0: 'First note',
    1: 'Second note'
}


class Note(Resource):
    def get(self, note_id):
        return notes[note_id]


api.add_resource(Note, "/note/<int:note_id>")

if __name__ == "__main__":
    app.run()
