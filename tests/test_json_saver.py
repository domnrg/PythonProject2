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


def write_vacancies(self, vacancies: list[dict]):
    """Сохраняет вакансии в JSON-файл, избегая дублирования по ссылке."""
    try:
        with open(self.__filename, encoding="utf-8") as f:
            existing_vacancies = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_vacancies = []

    # Преобразуем новые вакансии в нужный формат
    new_vacancies = []
    for vacancy in vacancies:
        new_vacancies.append({
            "name": vacancy.get("name"),
            "link": vacancy.get("alternate_url"),
            "salary": vacancy.get("salary"),
            "description": vacancy.get("snippet", {}).get("requirement"),
        })

    # Объединяем списки
    combined = existing_vacancies + new_vacancies

    # Удаляем дубликаты по ссылке
    unique_vacancies = []
    seen_links = set()
    for vac in combined:
        if vac["link"] not in seen_links:
            seen_links.add(vac["link"])
            unique_vacancies.append(vac)

    # Записываем обратно в файл
    with open(self.__filename, "w", encoding="utf-8") as f:
        json.dump(unique_vacancies, f, ensure_ascii=False, indent=4)


def test_delete_vacancies(saver, sample_vacancies):
    saver.write_vacancies(sample_vacancies)
    saver.delete_vacancies()

    with open(saver._JSONSaver__filename, encoding="utf-8") as f:
        data = json.load(f)
    assert data == []
