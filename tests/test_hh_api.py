from http.client import responses

from src.hh_api import HHApi
from unittest.mock import patch
from requests import Response


def test_get_vacancies_returns_list(fake_vacancies_response_page1, fake_vacancies_response_page2):
    hh = HHApi()

    # Подменяем _connect, чтобы при первом вызове вернуть page1, при втором — page2
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
