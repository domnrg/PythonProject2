from src.vacancy import Vacancy

def test_vacancy_with_salary():
    vacancy = Vacancy(
        name="Python Developer",
        link="https://hh.ru/vacancy/1",
        salary={"from": 100000, "to": 150000},
        description="Backend Python development"
    )
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.name == "Python Developer"

def test_vacancy_without_salary():
    vacancy = Vacancy(
        name="Data Analyst",
        link="https://hh.ru/vacancy/2",
        salary=None,
        description="Data analysis and reporting"
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0

def test_vacancy_partial_salary():
    vacancy = Vacancy(
        name="DevOps Engineer",
        link="https://hh.ru/vacancy/3",
        salary={"from": 80000},
        description="CI/CD and infrastructure"
    )
    assert vacancy.salary_from == 80000
    assert vacancy.salary_to == 0

def test_vacancy_comparison():
    v1 = Vacancy("Junior", "link1", {"from": 60000, "to": 80000}, "desc")
    v2 = Vacancy("Middle", "link2", {"from": 100000, "to": 130000}, "desc")
    assert v1 < v2

def test_vacancy_str():
    vacancy = Vacancy(
        name="QA Engineer",
        link="https://hh.ru/vacancy/4",
        salary={"from": 50000, "to": 70000},
        description="Testing and automation"
    )
    result = str(vacancy)
    assert "QA Engineer" in result
    assert "https://hh.ru/vacancy/4" in result
    assert "от 50000 до 70000" in result
