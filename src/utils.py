from src.hh_api import HeadHunterAPI


def get_from_api(search_text):
    """ Функция формирует список словарей из данных, полученных от API"""
    hh = HeadHunterAPI()
    all_info = []
    for text in search_text:
        employer_id = hh.get_employer_id_from_api(text)
        employer_info = hh.get_employer_info_from_api(employer_id)
        vacancies_info = hh.get_vacancies_from_api(employer_id)
        all_info.append({'employer_info': employer_info,
                         'vacancies_info': vacancies_info})

    return all_info


search_text = 'Pudov, Россельхозбанк'.split(', ')
print(search_text)
data = get_from_api(search_text)
print(data)
