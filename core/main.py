from bson import ObjectId

from core import app, api, mongo_db
from core.resources.note import Note
from core.resources.note_modify import NoteModify
from core.resources.notes import Notes


def note_exists(note_id):
    if not ObjectId.is_valid(note_id):
        return False
    return mongo_db.find_one({'_id': ObjectId(note_id)}) is not None


api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')
api.add_resource(NoteModify, '/api/note/<string:note_id>', endpoint='note-modify')

if __name__ == "__main__":
    app.run()
