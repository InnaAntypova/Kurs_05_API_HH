from src.db_manager import DBManager
from src.db_saver import DBSaver
from src.hh_api import HeadHunterAPI


def get_from_api(search_text: list[str]) -> list[dict]:
    """ Функция формирует список словарей из данных, полученных от API. """
    hh = HeadHunterAPI()
    all_info = []
    for text in search_text:
        employer_id = hh.get_employer_id_from_api(text)
        employer_info = hh.get_employer_info_from_api(employer_id)
        vacancies_info = hh.get_vacancies_from_api(employer_id)
        all_info.append({'employer_info': employer_info,
                         'vacancies_info': vacancies_info})
    return all_info


def write_data_to_db(data: list[dict]) -> None:
    """ Функция создаст и запишет данные в таблицы. """
    db = DBSaver()
    db.create_db()
    db.create_tables()
    db.save_data_to_database(data)


def get_companies_and_vacancies_count() -> None:
    """ Функция выводит пользователю название компании и ее вакансии. """
    hh = DBManager()
    data = hh.get_companies_and_vacancies_count()
    for item in data:
        print(f"Название компании: {item[0]}\nКоличество открытых вакансий: {item[1]}")
        print("")
        print("")


def get_all_vacancies() -> None:
    """ Функция выводит пользователю все вакансии. """
    hh = DBManager()
    data = hh.get_all_vacancies()
    for item in data:
        print(f"Название компании: {item[0]}\nНазвание вакансии: {item[1]}\nЗарплата: {item[2]} - {item[3]} рублей\n"
              f"Ссылка на вакансию: {item[4]}")
        print("")
        print("")


def get_avg_salary() -> None:
    """ Функция выводит пользователю величину средней зарплаты. """
    hh = DBManager()
    data = hh.get_avg_salary()
    print(f"Средняя заработная плата составляет {round(data[0])} рублей.")
    print("")
    print("")


def get_vacancies_with_higher_salary() -> None:
    """ Функция выводит пользователю вакансии с зарплатой выше средней. """
    hh = DBManager()
    data = hh.get_vacancies_with_higher_salary()
    for item in data:
        print(f"Название компании: {item[0]}\nНазвание вакансии: {item[1]}\nЗарплата: {item[2]} - {item[3]} рублей\n"
              f"Ссылка на вакансию: {item[4]}")
        print("")
        print("")


def get_vacancies_with_keyword(user_words: list[str]) -> None:
    """ Функция выводит вакансии по пользовательскому запросу. """
    hh = DBManager()
    for word in user_words:
        data = hh.get_vacancies_with_keyword(word)
        for item in data:
            print(f"Название компании: {item[0]}\nНазвание вакансии: {item[1]}\nЗарплата: {item[2]} - {item[3]} рублей\n"
                  f"Адрес: {item[4]}\nТип занятости: {item[5]}\nТребования: {item[6]}\nОбязанности: {item[7]}\n"
                  f"Ссылка на вакансию: {item[8]}")
            print("")
            print("")
