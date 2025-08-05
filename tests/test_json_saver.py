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
    # Записываем вакансии
    saver.write_vacancies(sample_vacancies)

    # Читаем вакансии
    vacancies = saver.read_vacancies()

    assert isinstance(vacancies, list)
    assert len(vacancies) == 2
    assert all(isinstance(vac, Vacancy) for vac in vacancies)

    # Проверяем данные первой вакансии
    first = vacancies[0]
    assert first.name == "Python Developer"
    assert first.link == "https://hh.ru/vacancy/123"
    assert first.salary_from == 100000

    # Проверяем данные второй вакансии (без зарплаты)
    second = vacancies[1]
    assert second.name == "Data Scientist"
    assert second.salary_from == 0  # валидируется в Vacancy


def test_write_vacancies_no_duplicates(saver, sample_vacancies):
    # Записываем первый раз
    saver.write_vacancies(sample_vacancies)

    # Записываем с дубликатом и новой вакансией
    new_vacancies = [
        {
            "name": "Python Developer",  # Дубликат по ссылке
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Опыт от 3 лет"},
        },
        {
            "name": "Frontend Developer",
            "alternate_url": "https://hh.ru/vacancy/789",
            "salary": {"from": 90000, "to": 120000},
            "snippet": {"requirement": "React, JS"},
        },
    ]
    saver.write_vacancies(new_vacancies)

    # Считываем и проверяем, что дубликат не добавился
    with open(saver._JSONSaver__filename, encoding="utf-8") as f:
        data = json.load(f)

    links = [vac["link"] for vac in data]
    assert len(data) == 3
    assert "https://hh.ru/vacancy/123" in links
    assert "https://hh.ru/vacancy/789" in links


def test_delete_vacancies(saver, sample_vacancies):
    saver.write_vacancies(sample_vacancies)
    saver.delete_vacancies()

    with open(saver._JSONSaver__filename, encoding="utf-8") as f:
        data = json.load(f)

    assert data == []


def test_read_vacancies_file_not_exist(tmp_path):
    # Тестируем чтение, когда файла нет
    file_path = tmp_path / "nonexistent.json"
    saver = JSONSaver(filename=str(file_path))

    # Файл не существует, метод должен вернуть пустой список без ошибки
    with pytest.raises(FileNotFoundError):
        saver.read_vacancies()
