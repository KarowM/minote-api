from bson.objectid import ObjectId
from flask_restful import Resource, reqparse, abort

from core import app, api, mongo_db
from core.resources.note import Note
from core.resources.notes import Notes

NOTE_BODY_CHAR_LIMIT = 250
NOTE_TITLE_CHAR_LIMIT = 30

# HTTP response codes
OK = 200
CREATED = 201
NO_CONTENT = 204
BAD_REQUEST = 400
NOT_FOUND = 404

note_patch_args = reqparse.RequestParser()
note_patch_args.add_argument('title', type=str)
note_patch_args.add_argument('body', type=str)


def note_exists(note_id):
    if not ObjectId.is_valid(note_id):
        return False
    return mongo_db.find_one({'_id': ObjectId(note_id)}) is not None


class NoteModify(Resource):
    def patch(self, note_id):
        if not note_exists(note_id):
            abort(NOT_FOUND, message=f"Could not find note with id {note_id}")

        args = note_patch_args.parse_args()
        title = args['title']
        body = args['body']
        if title is None and body is None:
            abort(BAD_REQUEST, message=f"Must provide at least title or body to patch note with id {note_id}")
        if title:
            if len(title) > NOTE_TITLE_CHAR_LIMIT:
                abort(BAD_REQUEST, message='Title length cannot exceed 30 characters')
            note = mongo_db.find_one({'_id': ObjectId(note_id)})
            note['title'] = title
            mongo_db.save(note)
        if body:
            if len(body) > NOTE_BODY_CHAR_LIMIT:
                abort(BAD_REQUEST, message='Body length cannot exceed 250 characters')
            note = mongo_db.find_one({'_id': ObjectId(note_id)})
            note['body'] = body
            mongo_db.save(note)

        return args, OK

    def delete(self, note_id):
        if not note_exists(note_id):
            abort(NOT_FOUND, message=f"Could not find note with id {note_id}")

        mongo_db.delete_one({'_id': ObjectId(note_id)})
        return '', NO_CONTENT


api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')
api.add_resource(NoteModify, '/api/note/<string:note_id>', endpoint='note-modify')

if __name__ == "__main__":
    app.run()
