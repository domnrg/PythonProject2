import json
import pytest
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies():
    return [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Опыт от 3 лет"},
        },
        {
            "name": "Data Scientist",
            "alternate_url": "https://hh.ru/vacancy/456",
            "salary": None,
            "snippet": {"requirement": "Python, ML, статистика"},
        },
    ]


@pytest.fixture
def saver(tmp_path):
    file_path = tmp_path / "vacancies.json"
    return JSONSaver(filename=str(file_path))


def test_write_and_read_vacancies(saver, sample_vacancies):
    # записываем
    saver.write_vacancies(sample_vacancies)

    # читаем
    read = saver.read_vacancies()

    assert isinstance(read, list)
    assert len(read) == 2
    assert all(isinstance(v, Vacancy) for v in read)
    assert read[0].name == "Python Developer"
    assert read[1].salary_from == 0


def test_delete_vacancies(saver, sample_vacancies):
    saver.write_vacancies(sample_vacancies)
    saver.delete_vacancies()

    with open(saver._JSONSaver__filename, encoding="utf-8") as f:
        data = json.load(f)
    assert data == []
