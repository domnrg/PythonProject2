import pytest
from unittest.mock import patch
from src.vacancy import Vacancy
from main import user_interaction


@pytest.fixture
def fake_vacancies():
    return [
        Vacancy("Python Dev", "https://hh.ru/vac1", {"from": 150000, "to": 200000}, "Разработка на Python"),
        Vacancy("Data Scientist", "https://hh.ru/vac2", {"from": 120000, "to": 160000}, "ML и анализ данных"),
        Vacancy("Backend Dev", "https://hh.ru/vac3", {"from": 100000, "to": 140000}, "Python разработка бэкенда"),
    ]


def test_user_interaction(monkeypatch, capsys, fake_vacancies):
    # Эмуляция ввода пользователя
    user_inputs = iter([
        "python",      # Поисковый запрос
        "2",           # Топ N
        "разработка",  # Ключевое слово
        "нет"          # Сохранять в файл?
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    # Подмена API и сохранения в файл
    with patch("main.HHApi.get_vacancies") as mock_get, \
         patch("main.JSONSaver.write_vacancies") as mock_write:

        mock_get.return_value = [
            {
                "name": vac.name,
                "alternate_url": vac.link,
                "salary": {"from": vac.salary_from, "to": vac.salary_to},
                "snippet": {"requirement": vac.description}
            }
            for vac in fake_vacancies
        ]

        user_interaction()
        output = capsys.readouterr().out

    # Проверки
    assert "Топ-2 вакансий по зарплате:" in output
    assert "Python Dev" in output
    assert "Backend Dev" in output
    assert "Средняя зарплата по найденным вакансиям" in output
    assert "Вакансии сохранены в файл" not in output  # тк "нет"
