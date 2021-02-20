from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

note_post_args = reqparse.RequestParser()
note_post_args.add_argument('title', type=str, help='Title of note is missing', required=True)
note_post_args.add_argument('body', type=str)

nextPos = 2
notes = {
    0: {
        'title': 'First note',
        'body': 'Body of first note'
    },
    1: {
        'title': 'Second note',
        'body': 'Body of second note'
    }
}


class Note(Resource):
    def post(self):
        global nextPos
        args = note_post_args.parse_args()
        note_note = {
            'title': args['title'],
            'body': args['body']
        }
        notes[nextPos] = note_note
        nextPos = nextPos + 1
        return note_note


class Notes(Resource):
    def get(self):
        return notes


api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')

if __name__ == "__main__":
    app.run()
