import unittest
from unittest.mock import patch, Mock

import werkzeug
from bson import ObjectId

import core.resources.note_modify
from core.resources.note_modify import NoteModify
from core.util import constants


class TestCases(unittest.TestCase):

    @patch('core.resources.note_modify.ObjectId')
    def test_note_exists_should_return_false_if_note_id_is_invalid(self, mock_object_id):
        mock_object_id.is_valid.return_value = False

        note_modify = NoteModify()
        actual_note_existence = note_modify.note_exists('1')

        self.assertFalse(actual_note_existence)

    @patch('core.resources.note_modify.ObjectId')
    @patch('core.resources.note_modify.mongo_db')
    def test_note_exists_should_return_false_if_note_id_does_not_exist(self, mock_mongo_db, mock_object_id):
        mock_object_id.is_valid.return_value = True
        mock_mongo_db.find_one.return_value = None

        note_modify = NoteModify()
        actual_note_existence = note_modify.note_exists('1')

        self.assertFalse(actual_note_existence)

    @patch('core.resources.note_modify.ObjectId')
    @patch('core.resources.note_modify.mongo_db')
    def test_note_exists_should_return_true_if_note_id_exists(self, mock_mongo_db, mock_object_id):
        mock_object_id.is_valid.return_value = True
        mock_mongo_db.find_one.return_value = {}

        note_modify = NoteModify()
        actual_note_existence = note_modify.note_exists('1')

        self.assertTrue(actual_note_existence)

    @patch.object(core.resources.note_modify.NoteModify, 'note_exists')
    def test_delete_returns_not_found_if_note_id_not_found(self, mock_note_exists):
        mock_note_exists.return_value = False

        note_modify = NoteModify()
        with self.assertRaises(werkzeug.exceptions.NotFound) as ctx:
            note_modify.delete('1')

        self.assertEqual(404, ctx.exception.code)
        self.assertEqual('Not Found', ctx.exception.name)

    @patch('core.resources.note_modify.mongo_db')
    @patch.object(core.resources.note_modify.NoteModify, 'note_exists')
    def test_delete_returns_not_found_if_note_id_not_found(self, mock_note_exists, mock_mongo_db):
        mock_note_exists.return_value = True
        note_id = '111111111111111111111111'

        note_modify = NoteModify()
        response = note_modify.delete(note_id)

        mock_mongo_db.delete_one.assert_called_with({'_id': ObjectId(note_id)})
        self.assertEqual(response, ('', constants.NO_CONTENT))

    @patch.object(core.resources.note_modify.NoteModify, 'note_exists')
    def test_patch_returns_not_found_if_note_id_not_found(self, mock_note_exists):
        mock_note_exists.return_value = False

        note_modify = NoteModify()
        with self.assertRaises(werkzeug.exceptions.NotFound) as ctx:
            note_modify.patch('1')

        self.assertEqual(404, ctx.exception.code)
        self.assertEqual('Not Found', ctx.exception.name)

    @patch.object(core.resources.note_modify.NoteModify, 'note_exists')
    def test_patch_returns_bad_request_if_title_and_body_are_not_found(self, mock_note_exists):
        mock_note_exists.return_value = True
        mock_req_parse = Mock()
        mock_req_parse.parse_args.return_value = {}
        NoteModify.note_patch_args = mock_req_parse

        note_modify = NoteModify()
        with self.assertRaises(werkzeug.exceptions.BadRequest) as ctx:
            note_modify.patch('1')

        self.assertEqual(400, ctx.exception.code)
        self.assertEqual('Bad Request', ctx.exception.name)
