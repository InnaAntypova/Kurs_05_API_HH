from typing import Any

import psycopg2
from src.config import config


class DBManager:
    """ Класс для получения и манипуляций с данными из PostgreSQL. """

    def __init__(self):
        """ Метод для инициализации класса. """
        self.params = config()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any]]:
        """ Метод получает список всех компаний и количество вакансий у каждой компании. """
        try:
            conn = psycopg2.connect(dbname='hh_info', **self.params)
            with conn.cursor() as cur:
                cur.execute("SELECT employers.employer_name, COUNT(vacancies.vacancy_id) FROM vacancies "
                            "JOIN employers USING(employer_id) GROUP BY employers.employer_name;")
                data = cur.fetchall()

            conn.commit()
            conn.close()
            return data

        except psycopg2.OperationalError:
            print("Ошибка данных")

    def get_all_vacancies(self) -> list[tuple[Any]]:
        """ Метод получает список всех вакансий. """
        try:
            conn = psycopg2.connect(dbname='hh_info', **self.params)
            with conn.cursor() as cur:
                cur.execute("SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, "
                            "vacancies.salary_to, vacancies.vacancy_url FROM vacancies "
                            "JOIN employers USING(employer_id) GROUP BY employers.employer_name, vacancies.vacancy_name, "
                            "vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url "
                            "ORDER BY employers.employer_name;")
                data = cur.fetchall()

            conn.commit()
            conn.close()
            return data

        except psycopg2.OperationalError:
            print("Ошибка данных")

    def get_avg_salary(self) -> tuple[Any]:
        """ Метод получает среднюю зарплату по вакансиям. """
        try:
            conn = psycopg2.connect(dbname='hh_info', **self.params)
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) FROM vacancies WHERE salary_from <> 0;")
                data = cur.fetchone()

            conn.commit()
            conn.close()
            return data

        except psycopg2.OperationalError:
            print("Ошибка данных")

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any]]:
        """ Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """
        try:
            conn = psycopg2.connect(dbname='hh_info', **self.params)
            with conn.cursor() as cur:
                cur.execute("SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, "
                            "vacancies.salary_to, vacancies.vacancy_url FROM vacancies JOIN employers "
                            "USING(employer_id) GROUP BY employers.employer_name, vacancies.vacancy_name, "
                            "vacancies.salary_from, vacancies.salary_to, vacancies.vacancy_url "
                            "HAVING vacancies.salary_from > (SELECT AVG(salary_from) FROM vacancies "
                            "WHERE salary_from <> 0) ORDER BY vacancies.salary_from;")
                data = cur.fetchall()

            conn.commit()
            conn.close()
            return data

        except psycopg2.OperationalError:
            print("Ошибка данных")

    def get_vacancies_with_keyword(self, word: str) -> list[tuple[Any]]:
        """ Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова. """
        try:
            conn = psycopg2.connect(dbname='hh_info', **self.params)
            with conn.cursor() as cur:
                cur.execute(f"SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, "
                            f"vacancies.salary_to, vacancies.address, vacancies.employment, vacancies.requirement, "
                            f"vacancies.responsibility, vacancies.vacancy_url FROM vacancies "
                            f"JOIN employers USING(employer_id) WHERE vacancy_name LIKE '%{word}%'")
                data = cur.fetchall()

            conn.commit()
            conn.close()
            return data

        except psycopg2.OperationalError:
            print("Ошибка данных")
