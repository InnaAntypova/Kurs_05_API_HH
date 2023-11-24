from src.utils import get_from_api, write_data_to_db, get_companies_and_vacancies_count, get_all_vacancies, \
    get_avg_salary, get_vacancies_with_higher_salary, get_vacancies_with_keyword


def main():
    search_text = 'BondSoft, DBI, FIRECODE, OnlyWork, RNDSOFT, МДЦ Эксперт, Правое дело, Электронная медицина, ' \
                  'Интеллектика, ДОНГИС'.split(', ')
    print(f"Программа сформирует для Вас вакансии определенных компаний: {', '.join(search_text)}")
    data = get_from_api(search_text)
    write_data_to_db(data)
    print("Данные сформированы.")
    while True:
        print("Нажмите '1' - просмотр всех компаний и кол-во открытых вакансий, '2' - просмотр всех вакансий, "
              "'3' - просмотр средней зарплаты по вакансиям, \n'4' - просмотр вакансий с зарплатой выше средней,"
              "'5' - просмотр вакансий по заданному поиску.")
        print("Для завершения программы нажмите '0'.")
        user_input = input("Ваш выбор: ")
        print("")

        if user_input == '1':
            get_companies_and_vacancies_count()

        if user_input == '2':
            get_all_vacancies()

        if user_input == '3':
            get_avg_salary()

        if user_input == '4':
            get_vacancies_with_higher_salary()

        if user_input == '5':
            user_words = input("Введите слова для поиска разделяя пробелом: ").lower().split(' ')
            get_vacancies_with_keyword(user_words)

        if user_input == '0':
            print("Программа завершена.")
            break


if __name__ == '__main__':
    main()
