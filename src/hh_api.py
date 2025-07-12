from abc import ABC, abstractmethod

import requests


class AbstractApi(ABC):
    """Абстрактный класс для взаимодействия с API платформ вакансий."""

    @abstractmethod
    def _connect(self, text):
        """Подключение к API."""
        pass

    @abstractmethod
    def get_vacancies(self, text):
        """Получение вакансий по ключевому слову."""
        pass


class HHApi(AbstractApi):
    """Класс для работы с API hh.ru."""

    def __init__(self, page=0, area_id="113"):
        """Инициализация параметров подключения к API hh.ru."""
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"page": page, "per_page": 30, "area": area_id}

    def _connect(self, text):
        """Отправка GET-запроса к API hh.ru с заданными параметрами."""
        self.__params["text"] = text
        response = requests.get(self.__url, params=self.__params)
        response.raise_for_status()
        return response

    def get_vacancies(self, text, page=2):
        """Получение списка вакансий по ключевому слову."""
        all_vacancies = []
        while self.__params["page"] < page:
            vacancies = self._connect(text).json()["items"]
            all_vacancies.extend(vacancies)
            self.__params["page"] += 1
        return all_vacancies


hh = HHApi()
print(hh.get_vacancies("python"))
