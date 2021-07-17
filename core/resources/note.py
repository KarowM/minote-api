from flask_restful import Resource, reqparse, abort
from core.util import constants
from core import mongo_db


class Note(Resource):
    note_post_args = reqparse.RequestParser()
    note_post_args.add_argument('title', type=str, help='Title of note is missing', required=True)
    note_post_args.add_argument('body', type=str)

    def post(self):
        args = Note.note_post_args.parse_args()
        title = args['title']
        body = args['body'] if args['body'] else ''
        if len(title) > constants.NOTE_TITLE_CHAR_LIMIT:
            abort(constants.BAD_REQUEST, message='Title length cannot exceed 30 characters')
        if len(body) > constants.NOTE_BODY_CHAR_LIMIT:
            abort(constants.BAD_REQUEST, message='Note body length cannot exceed 250 characters')
        new_note = {
            'title': title,
            'body': body
        }
        mongo_db.insert_one(new_note)
        new_note['_id'] = str(new_note.get('_id'))
        return new_note, constants.CREATED
