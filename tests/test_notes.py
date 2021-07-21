import unittest
from unittest.mock import patch

from bson import ObjectId

from core.resources.notes import Notes
from core.util import constants


class TestCases(unittest.TestCase):

    @patch('core.resources.notes.mongo_db')
    def test_get_should_return_empty_note_list_with_ok_status(self, mock_mongodb):
        mock_mongodb.find.return_value = []

        notes = Notes()
        get_response = notes.get()

        self.assertEqual(([], constants.OK), None)

    @patch('core.resources.notes.mongo_db')
    def test_get_should_return_note_list_with_ok_status(self, mock_mongodb):
        mock_mongodb.find.return_value = [
            {'_id': ObjectId('60f30e236c24bc528eb8a30b'), 'title': 'new title', 'body': 'new body'}
        ]

        expected_notes_list = [
            {'_id': '60f30e236c24bc528eb8a30b', 'title': 'new title', 'body': 'new body'}
        ]

        notes = Notes()
        get_response = notes.get()

        self.assertEqual((expected_notes_list, constants.OK), get_response)
