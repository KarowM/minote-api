from bson.objectid import ObjectId
from flask_restful import Resource, reqparse, abort

from core import mongo_db
from core.util import constants


class NoteModify(Resource):
    note_patch_args = reqparse.RequestParser()
    note_patch_args.add_argument('title', type=str)
    note_patch_args.add_argument('body', type=str)

    def note_exists(self, note_id):
        if not ObjectId.is_valid(note_id):
            return False
        return mongo_db.find_one({'_id': ObjectId(note_id)}) is not None

    def patch(self, note_id):
        if not self.note_exists(note_id):
            abort(constants.NOT_FOUND, message=f"Could not find note with id {note_id}")

        args = self.note_patch_args.parse_args()
        title = args['title']
        body = args['body']
        if title is None and body is None:
            abort(constants.BAD_REQUEST, message=f"Must provide at least title or body to patch note with id {note_id}")
        if title:
            if len(title) > constants.NOTE_TITLE_CHAR_LIMIT:
                abort(constants.BAD_REQUEST, message='Title length cannot exceed 30 characters')
            note = mongo_db.find_one({'_id': ObjectId(note_id)})
            note['title'] = title
            mongo_db.save(note)
        if body:
            if len(body) > constants.NOTE_BODY_CHAR_LIMIT:
                abort(constants.BAD_REQUEST, message='Body length cannot exceed 250 characters')
            note = mongo_db.find_one({'_id': ObjectId(note_id)})
            note['body'] = body
            mongo_db.save(note)

        return args, constants.OK

    def delete(self, note_id):
        if not self.note_exists(note_id):
            abort(constants.NOT_FOUND, message=f"Could not find note with id {note_id}")

        mongo_db.delete_one({'_id': ObjectId(note_id)})
        return '', constants.NO_CONTENT
