import unittest
from unittest.mock import Mock

import werkzeug

from core.resources.note import Note
from core.util import constants


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
