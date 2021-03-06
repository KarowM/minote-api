from flask_restful import Api, Resource, reqparse, abort
from __init__ import mongo_db
from __init__ import app

NOTE_BODY_CHAR_LIMIT = 250
NOTE_TITLE_CHAR_LIMIT = 30

# HTTP response codes
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
NOT_FOUND = 404

mongo_db.insert_one({
    'title': 'hello',
    'body': 'world'
})

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
        title = args['title']
        body = args['body'] if args['body'] else ''
        if len(title) > NOTE_TITLE_CHAR_LIMIT:
            abort(BAD_REQUEST, message='Title length cannot exceed 30 characters')
        if len(body) > NOTE_BODY_CHAR_LIMIT:
            abort(BAD_REQUEST, message='Note body length cannot exceed 250 characters')
        note_note = {
            'title': title,
            'body': body
        }
        notes[nextPos] = note_note
        nextPos = nextPos + 1
        return note_note, CREATED


class NoteModify(Resource):
    def patch(self, note_id):
        if note_id not in notes:
            abort(NOT_FOUND, message=f"Could not find note with id {note_id}")

        args = note_patch_args.parse_args()
        title = args['title']
        body = args['body']
        if title is None and body is None:
            abort(BAD_REQUEST, message=f"Must provide at least title or body to patch note with id {note_id}")
        if title:
            if len(title) > NOTE_TITLE_CHAR_LIMIT:
                abort(BAD_REQUEST, message='Title length cannot exceed 30 characters')
            notes[note_id]['title'] = title
        if body:
            if len(body) > NOTE_BODY_CHAR_LIMIT:
                abort(BAD_REQUEST, message='Body length cannot exceed 250 characters')
            notes[note_id]['body'] = body

        return args, OK

    def delete(self, note_id):
        if note_id not in notes:
            abort(NOT_FOUND, message=f"Could not find note with id {note_id}")

        notes.pop(note_id)
        return '', NO_CONTENT


class Notes(Resource):
    def get(self):
        return notes, OK

api = Api(app)
api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')
api.add_resource(NoteModify, '/api/note/<int:note_id>', endpoint='note-modify')

if __name__ == "__main__":
    app.run()
