import psycopg2
from src.config import config


class DBSaver:
    """ Класс для сохранения данных в PostgreSQL. """
    params = config()

    def create_db(self) -> None:
        """ Метод для создания базы данных. """
        conn = psycopg2.connect(dbname='postgres', **DBSaver.params)
        conn.autocommit = True
        cursor = conn.cursor()
        # удалим базу, если такая уже есть
        cursor.execute('DROP DATABASE IF EXISTS hh_info')
        cursor.execute('CREATE DATABASE hh_info')
        cursor.close()
        conn.close()

    def create_tables(self) -> None:
        """ Метод для создания таблиц в базе данных. """
        conn = psycopg2.connect(dbname='hh_info', **DBSaver.params)
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers ('
                        'employer_id SERIAL PRIMARY KEY,'
                        'employer_name VARCHAR(255) NOT NULL,'
                        'description TEXT NOT NULL,'
                        'employer_url TEXT)')

        with conn.cursor() as cur:
            cur.execute('CREATE TABLE vacancies ('
                        'vacancy_id SERIAL PRIMARY KEY,'
                        'employer_id INT REFERENCES employers(employer_id),'
                        'vacancy_name VARCHAR(255) NOT NULL,'
                        'area VARCHAR(50),'
                        'address VARCHAR(100),'
                        'salary_from INT,'
                        'salary_to INT,'
                        'published DATE NOT NULL,'
                        'employment VARCHAR(25),'
                        'requirement TEXT,'
                        'responsibility TEXT,'
                        'vacancy_url TEXT)')

        conn.commit()
        conn.close()

    def save_data_to_database(self, all_info) -> None:
        """ Сохранение данных о работодателях и их вакансиях. """
        conn = psycopg2.connect(dbname='hh_info', **DBSaver.params)
        with conn.cursor() as cur:
            for employer in all_info:
                employer_data = employer['employer_info']
                for data in employer_data:
                    cur.execute("INSERT INTO employers (employer_name, description, employer_url) VALUES (%s, %s, %s) "
                                "RETURNING employer_id", (data['name'], data['description'], data['employer_url']))

                    employer_id = cur.fetchone()
                    vacancies = employer['vacancies_info']
                    for vacancy in vacancies:
                        cur.execute("INSERT INTO vacancies (employer_id, vacancy_name, area, address, salary_from, "
                                    "salary_to, published, employment, requirement, responsibility, vacancy_url) VALUES "
                                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (employer_id,
                                                                                     vacancy['vacancy_name'],
                                                                                     vacancy['area'],
                                                                                     vacancy['address'],
                                                                                     vacancy['salary_from'],
                                                                                     vacancy['salary_to'],
                                                                                     vacancy['published'],
                                                                                     vacancy['employment'],
                                                                                     vacancy['requirement'],
                                                                                     vacancy['responsibility'],
                                                                                     vacancy['vacancy_url']))

        conn.commit()
        conn.close()
