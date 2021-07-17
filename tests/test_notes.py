import unittest
from unittest.mock import patch
from core.resources.notes import Notes
from core.util import constants


class TestCases(unittest.TestCase):

    @patch('core.resources.notes.mongo_db')
    def test_get(self, mock_mongodb):
        mock_mongodb.find.return_value = []

        notes = Notes()
        get_response = notes.get()

        self.assertEqual(([], constants.OK), get_response)
