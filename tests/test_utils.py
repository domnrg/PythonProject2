import pytest
from src.utils import (
    convert_dict_to_vacancy,
    filter_by_keyword,
    get_top_vacancies,
    calculate_average_salary,
    print_vacancies
)
from src.vacancy import Vacancy

@pytest.fixture
def sample_vacancy_dict():
    return {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "snippet": {"requirement": "Опыт с Django и Flask"},
    }

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Dev A", "url1", {"from": 50000, "to": 80000}, "описание A"),
        Vacancy("Dev B", "url2", {"from": 100000, "to": 120000}, "описание B"),
        Vacancy("Dev C", "url3", {"from": 70000, "to": 100000}, "описание C"),
    ]

def test_convert_dict_to_vacancy(sample_vacancy_dict):
    vacancy = convert_dict_to_vacancy(sample_vacancy_dict)
    assert isinstance(vacancy, Vacancy)
    assert vacancy.name == "Python Developer"
    assert vacancy.link == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000

def test_filter_by_keyword(sample_vacancies):
    result = filter_by_keyword(sample_vacancies, "описание b")
    assert len(result) == 1
    assert result[0].name == "Dev B"

def test_get_top_vacancies(sample_vacancies):
    top = get_top_vacancies(sample_vacancies, 2)
    assert len(top) == 2
    assert top[0].salary_from >= top[1].salary_from

def test_calculate_average_salary(sample_vacancies):
    avg = calculate_average_salary(sample_vacancies)
    assert avg == (50000 + 100000 + 70000) // 3

def test_print_vacancies_output(sample_vacancies, capsys):
    print_vacancies(sample_vacancies)
    captured = capsys.readouterr()
    assert "Dev A" in captured.out
    assert "-" * 50 in captured.out
