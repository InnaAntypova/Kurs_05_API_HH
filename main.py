
from src.utils import get_from_api, write_data_to_db



def main():
    search_text = 'Pudov, Россельхозбанк'.split(', ')
    print(f"Программа сформирует для Вас вакансии определенных компаний: {', '.join(search_text)}")
    data = get_from_api(search_text)
    write_data_to_db(data)


if __name__ == '__main__':
    main()
