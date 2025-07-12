from abc import ABC, abstractmethod

import requests


class AbstractApi(ABC):

    @abstractmethod
    def _connect(self, text):
        pass

    @abstractmethod
    def get_vacancies(self,text):
        pass

class  HHApi(AbstractApi):
    def __init__(self, page=0):
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"page": page, "per_page": 30}

    def _connect(self, text):
        self.__params["text"] = text
        response = requests.get(self.__url, params=self.__params)
        response.raise_for_status()
        return response

    def get_vacancies(self, text):
        vacancies = self._connect(text).json()["items"]
        return vacancies


hh = HHApi()
print(hh.get_vacancies("python"))