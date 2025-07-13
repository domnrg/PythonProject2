import pytest
from unittest.mock import Mock

@pytest.fixture
def fake_vacancies_response_page1():
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {
        "items": [
            {"id": "1", "name": "Python Dev"},
            {"id": "2", "name": "Data Analyst"},
        ]
    }
    return mock_response

@pytest.fixture
def fake_vacancies_response_page2():
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {
        "items": [
            {"id": "3", "name": "Java Dev"},
            {"id": "4", "name": "System Admin"},
        ]
    }
    return mock_response