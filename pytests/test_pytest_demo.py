import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
from pytest_demo import process_data_from_file

@pytest.fixture
def mock_file_content():
    return {
        "api_key": "12345abcde"
    }

def test_process_data_from_file(mock_file_content):

    mock_file = mock_open(read_data=json.dumps(mock_file_content))
    with patch("builtins.open", mock_file):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"status": "success", "message": "data received"}
            mock_get.return_value = mock_response
            result = process_data_from_file("api_config.json", "Hello")
            
            mock_file.assert_called_once_with("api_config.json", 'r')
            
            mock_get.assert_called_once_with(
                "https://api.example.com/data", 
                headers={"Authorization": "Bearer 12345abcde"},
                params={"message": "Hello"}
            )
            assert result == {"status": "success", "message": "data received"}