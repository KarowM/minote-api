import unittest
from unittest.mock import patch

from core.resources.note_modify import NoteModify


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
