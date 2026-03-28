import unittest
from unittest.mock import Mock, patch
import requests

from user_service import get_user_full_name


class TestGetUserFullName(unittest.TestCase):

    @patch('user_service.requests.get')
    def test_get_user_full_name_success(self, mock_get):
     
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        result = get_user_full_name(1)

        self.assertEqual(result, "John Doe")
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch('user_service.requests.get')
    def test_get_user_full_name_not_found(self, mock_get):
      
        mock_response = Mock()
        mock_response.status_code = 404

        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mock_get.return_value = mock_response

        result = get_user_full_name(999)

        self.assertIsNone(result)
        mock_get.assert_called_once_with("https://api.example.com/users/999")

    @patch('user_service.requests.get')
    def test_get_user_full_name_server_error(self, mock_get):
     
        mock_response = Mock()
        mock_response.status_code = 500

        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mock_get.return_value = mock_response

        result = get_user_full_name(1)

        self.assertEqual(result, "Server error")
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch('user_service.requests.get')
    def test_get_user_full_name_network_error(self, mock_get):
      
        mock_get.side_effect = requests.exceptions.RequestException

        result = get_user_full_name(1)

        self.assertEqual(result, "Network error")
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch('user_service.requests.get')
    def test_get_user_full_name_other_http_error(self, mock_get):
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mock_get.return_value = mock_response

        result = get_user_full_name(1)

        self.assertEqual(result, "Server error")
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch('user_service.requests.get')
    def test_get_user_full_name_missing_name_fields(self, mock_get):
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        result = get_user_full_name(1)

        self.assertEqual(result, "None None")
        mock_get.assert_called_once_with("https://api.example.com/users/1")


if __name__ == '__main__':
    unittest.main()
