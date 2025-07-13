class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("name", "link", "salary_from", "salary_to", "description")

    def __init__(self, name, link, salary, description):
        """Инициализирует объект Vacancy, валидируя зарплату."""
        self.name = name
        self.link = link
        self.description = description
        self.__validate(salary)

    def __validate(self, salary: dict | None):
        """Приватный метод для валидации данных о зарплате."""
        if salary:
            self.salary_from = salary.get("from") or 0
            self.salary_to = salary.get("to") or 0
        else:
            self.salary_from = 0
            self.salary_to = 0

    def __lt__(self, other):
        """Сравнение вакансий по нижней границе зарплаты."""
        return self.salary_from < other.salary_from

    def __eq__(self, other):
        return self.salary_from == other.salary_from

    def __gt__(self, other):
        return self.salary_from > other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def __ge__(self, other):
        return self.salary_from >= other.salary_from

    def __ne__(self, other):
        return self.salary_from != other.salary_from

    def __str__(self):
        """Возвращает строковое представление объекта Vacancy."""
        return (
            f"Название: {self.name}\n"
            f"Ссылка: {self.link}\n"
            f"Описание: {self.description}\n"
            f"Зарплата: от {self.salary_from} до {self.salary_to}"
        )
