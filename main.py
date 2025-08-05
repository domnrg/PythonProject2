from src.json_saver import JSONSaver
from src.hh_api import HHApi
from src.utils import convert_dict_to_vacancy, filter_by_keyword, get_top_vacancies, calculate_average_salary


def user_interaction():
    """Основная функция взаимодействия с пользователем."""
    query = input("Введите поисковый запрос для поиска вакансий: ")
    hh = HHApi()
    vacancies_dicts = hh.get_vacancies(query)

    # Сохраняем список как объектов Vacancy
    vacancies = [convert_dict_to_vacancy(vac) for vac in vacancies_dicts]

    # Топ N по зарплате
    while True:
        try:
            top_n = int(input("Сколько вакансий с наивысшей зарплатой вы хотите увидеть? ").strip().strip("'\""))
            break
        except ValueError:
            print("Введите корректное число!")
    top_vacancies = get_top_vacancies(vacancies, top_n)
    print(f"\nТоп-{top_n} вакансий по зарплате:")
    for vac in top_vacancies:
        print(vac)

    # Фильтрация по ключевому слову
    keyword = input("Введите ключевое слово для фильтрации по описанию: ")
    filtered = filter_by_keyword(vacancies, keyword)
    print(f"\nВакансии, содержащие '{keyword}' в описании:")
    for vac in filtered:
        print(vac)

    # Средняя зарплата
    avg_salary = calculate_average_salary(vacancies)
    print(f"\n Средняя зарплата по найденным вакансиям: {avg_salary} руб.")

    # Сохранение в файл
    save = input("Хотите сохранить найденные вакансии в файл? (да/нет): ").lower()
    if save == "да":
        json_saver = JSONSaver()
        json_saver.write_vacancies(vacancies_dicts)
        print("Вакансии сохранены в файл.")


if __name__ == "__main__":
    user_interaction()
