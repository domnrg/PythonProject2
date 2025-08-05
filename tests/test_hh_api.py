import pytest

from src.hh_api import HHApi
from unittest.mock import patch, Mock
from requests import Response


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


def test_get_vacancies_returns_list(fake_vacancies_response_page1, fake_vacancies_response_page2):
    hh = HHApi()

    with patch.object(hh, "_connect", side_effect=[fake_vacancies_response_page1, fake_vacancies_response_page2]):
        result = hh.get_vacancies("python", page=2)
        print("RESULT:", result)
        assert isinstance(result, list)
        assert len(result) == 4
        assert result[0]["id"] == "1"
        assert result[-1]["id"] == "4"


@patch("requests.get")
def test_connect(mock_get):
    hh = HHApi()
    response = Response()
    response.status_code = 200
    mock_get.return_value = response
    result = hh._connect("test")
    assert result is response
    assert result.status_code == 200
    mock_get.assert_called_once()
