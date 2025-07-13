import json
from abc import ABC, abstractmethod

from src.vacancy import Vacancy


class AbstractJson(ABC):
    """Абстрактный базовый класс для работы с хранилищем вакансий."""

    @abstractmethod
    def write_vacancies(self):
        """Записывает список вакансий в хранилище."""
        pass

    @abstractmethod
    def read_vacancies(self):
        """Читает список вакансий из хранилища."""
        pass

    @abstractmethod
    def delete_vacancies(self):
        """Удаляет все вакансии из хранилища."""
        raise NotImplementedError


class JSONSaver(AbstractJson):
    """Класс для сохранения и загрузки вакансий в JSON-файл."""
    def __init__(self, filename="data/vacancies.json"):
        self.__filename = filename

    def write_vacancies(self, vacancies: list[dict]):
        """Сохраняет отфильтрованный список вакансий в JSON-файл."""
        vacancies_filter = []
        for vacancy in vacancies:
            vacancies_filter.append(
                {
                    "name": vacancy.get("name"),
                    "link": vacancy.get("alternate_url"),
                    "salary": vacancy.get("salary"),
                    "description": vacancy.get("snippet", {}).get("requirement")
                }
            )
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(vacancies_filter, f, ensure_ascii=False, indent=4)

    def read_vacancies(self):
        """Загружает вакансии из JSON-файла и преобразует их в объекты Vacancy"""
        with open(self.__filename, encoding="utf-8") as f:
            data = json.load(f)
        vacancies = []
        for vacancy in data:
            vacancies.append(Vacancy(**vacancy))
        return vacancies

    def delete_vacancies(self):
        """Очищает содержимое JSON-файла (удаляет все вакансии)."""
        with open(self.__filename, "w") as f:
            json.dump([], f)
