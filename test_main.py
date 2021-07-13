import unittest
from unittest.mock import patch
from core.main import note_exists


class TestSum(unittest.TestCase):

    @patch('core.main.ObjectId')
    def test_note_exists_should_return_false_if_note_id_is_invalid(self, mock_object_id):
        mock_object_id.is_valid.return_value = False

        actual_note_existence = note_exists('1')

        self.assertFalse(actual_note_existence)

    @patch('core.main.ObjectId')
    @patch('core.main.mongo_db')
    def test_note_exists_should_return_false_if_note_id_does_not_exist(self, mock_mongo_db, mock_object_id):
        mock_object_id.is_valid.return_value = True
        mock_mongo_db.find_one.return_value = None

        actual_note_existence = note_exists('1')

        self.assertFalse(actual_note_existence)

    @patch('core.main.ObjectId')
    @patch('core.main.mongo_db')
    def test_note_exists_should_return_true_if_note_id_exists(self, mock_mongo_db, mock_object_id):
        mock_object_id.is_valid.return_value = True
        mock_mongo_db.find_one.return_value = {}

        actual_note_existence = note_exists('1')

        self.assertTrue(actual_note_existence)


if __name__ == '__main__':
    unittest.main()
