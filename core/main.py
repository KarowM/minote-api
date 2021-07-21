from core import app, api
from core.resources.note import Note
from core.resources.note_modify import NoteModify
from core.resources.notes import Notes

api.add_resource(Notes, '/api/notes', endpoint='all-notes')
api.add_resource(Note, '/api/note', endpoint='note')
api.add_resource(NoteModify, '/api/note/<string:note_id>', endpoint='note-modify')

if __name__ == "__main__":
    app.run()
