from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

note_post_args = reqparse.RequestParser()
note_post_args.add_argument('title', type=str, help='Title of note is missing', required=True)
note_post_args.add_argument('body', type=str)

note_patch_args = reqparse.RequestParser()
note_patch_args.add_argument('title', type=str)
note_patch_args.add_argument('body', type=str)

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
        body = args['body'] if args['body'] else ''
        note_note = {
            'title': args['title'],
            'body': body
        }
        notes[nextPos] = note_note
        nextPos = nextPos + 1
        return note_note, 201


class NoteModify(Resource):
    def patch(self, note_id):
        if note_id not in notes:
            abort(404, message=f"Could not find note with id {note_id}")

        args = note_patch_args.parse_args()
        if args['title'] is None and args['body'] is None:
            abort(400, message=f"Must provide at least title or body to patch note with id {note_id}")
        if args['title']:
            notes[note_id]['title'] = args['title']
        if args['body']:
            notes[note_id]['body'] = args['body']

        return args, 200

    def delete(self, note_id):
        if note_id not in notes:
            abort(404, message=f"Could not find note with id {note_id}")

        notes.pop(note_id)
        return '', 204


class Notes(Resource):
    def get(self):
        return notes, 200


api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')
api.add_resource(NoteModify, '/api/note/<int:note_id>', endpoint='note-modify')

if __name__ == "__main__":
    app.run()
