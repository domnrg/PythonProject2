from src.json_saver import JSONSaver
from src.hh_api import HHApi


hh = HHApi()
vacancies = hh.get_vacancies("python")
json_saver = JSONSaver()
json_saver.write_vacancies(vacancies)


vacs = json_saver.read_vacancies()
for vac in vacs:
    print(vac)
