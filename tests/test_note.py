import unittest
from unittest.mock import Mock, patch

import werkzeug
from bson import ObjectId

from core.resources.note import Note
from core.util import constants


def mocked_mongo_insert(note):
    note['_id'] = ObjectId('111111111111111111111111')
    return note


class TestCases(unittest.TestCase):

    def test_post_returns_bad_request_if_title_is_too_long(self):
        mock_req_parse = Mock()
        mock_req_parse.parse_args.return_value = {
            'title': 'a' * (constants.NOTE_TITLE_CHAR_LIMIT + 1),
            'body': 'new body'
        }
        Note.note_post_args = mock_req_parse

        note = Note()
        with self.assertRaises(werkzeug.exceptions.BadRequest) as ctx:
            note.post()

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual('Bad Request', ctx.exception.name)

    def test_post_returns_bad_request_if_body_is_too_long(self):
        mock_req_parse = Mock()
        mock_req_parse.parse_args.return_value = {
            'title': 'new title',
            'body': 'a' * (constants.NOTE_BODY_CHAR_LIMIT + 1)
        }
        Note.note_post_args = mock_req_parse

        note = Note()
        with self.assertRaises(werkzeug.exceptions.BadRequest) as ctx:
            note.post()

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual('Bad Request', ctx.exception.name)

    @patch('core.resources.note.mongo_db')
    def test_post_returns_created_note_and_response_code(self, mock_mongo_db):
        mock_req_parse = Mock()
        mock_req_parse.parse_args.return_value = {
            'title': 'new title',
            'body': 'new body'
        }
        mock_mongo_db.insert_one.side_effect = mocked_mongo_insert

        Note.note_post_args = mock_req_parse
        note = Note()
        response = note.post()

        expected_response = {'title': 'new title', 'body': 'new body', '_id': '111111111111111111111111'}
        mock_mongo_db.insert_one.assert_called_with(expected_response)

        self.assertEqual(response, (expected_response, constants.CREATED))
