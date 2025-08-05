from src.vacancy import Vacancy


def convert_dict_to_vacancy(data: dict) -> Vacancy:
    """Конвертация словаря в экземпляр класса Vacancy."""
    return Vacancy(
        name=data["name"],
        link=data["alternate_url"],
        salary=data.get("salary"),
        description=(data.get("snippet", {}).get("requirement") or "Нет описания"),
    )


def filter_by_keyword(vacancies: list[Vacancy], keyword: str):
    """Фильтрация вакансий по ключевому слову в описании."""
    return [vac for vac in vacancies if isinstance(vac.description, str) and keyword.lower() in vac.description.lower()]


def get_top_vacancies(vacancies: list[Vacancy], top_n: int):
    """Сортирует вакансии по убыванию начальной зарплаты."""
    return sorted(vacancies, reverse=True)[:top_n]


def calculate_average_salary(vacancies: list) -> int:
    """Вычисление средней зарплаты по найденным вакансиям."""
    salaries = [v.salary_from for v in vacancies if isinstance(v.salary_from, int) and v.salary_from > 0]
    return sum(salaries) // len(salaries) if salaries else 0

def print_vacancies(vacancies: list[Vacancy]):
    """Печатает список вакансий."""
    for vac in vacancies:
        print(vac)
        print("-" * 50)
