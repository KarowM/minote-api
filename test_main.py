import unittest
from unittest.mock import patch
from core.main import note_exists


class TestSum(unittest.TestCase):

    @patch('core.main.ObjectId')
    def test_note_exists(self, mock_object_id):
        mock_object_id.is_valid.return_value = False

        actual_note_existance = note_exists(1)

        self.assertFalse(actual_note_existance)


if __name__ == '__main__':
    unittest.main()
