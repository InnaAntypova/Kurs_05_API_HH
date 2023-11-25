from typing import Any

from src.abc_api import ABCApi
import requests
from datetime import datetime


class HeadHunterAPI(ABCApi):
    """ Класс для работы с API сайта HH.ru """

    HH_url = "https://api.hh.ru/employers"

    headers = {"User-Agent": "HH-User-Agent"}

    def get_employer_id_from_api(self, text: str) -> str:
        """ Метод для получения ID работодателя по текстовому названию компании и информации о нем от API. """
        param = {
            'only_with_vacancies': True,
            'sort_by': 'by_vacancies_open',
            'page': 0,
            'per_page': 20,
            'text': text
        }

        employer_id = requests.get(url=HeadHunterAPI.HH_url, headers=HeadHunterAPI.headers,
                                   params=param, timeout=10).json()['items'][0]['id']
        return employer_id

    def get_employer_info_from_api(self, employer_id: str) -> list[dict[str, Any]]:
        """ Метод для получения информации о работодателе по его ID. """
        employer_url = f"https://api.hh.ru/employers/{employer_id}"
        data = requests.get(url=employer_url, headers=HeadHunterAPI.headers, timeout=10).json()

        employer_info = []
        try:
            name = data['name']
            description = data['description'].replace('<p>', '').replace('<strong>', '').replace('</p>', ''). \
                replace('</strong>', '').replace('&ndash;', '').replace(';&ndash;', '').replace('&nbsp;', '').\
                replace('<br />', '').replace('</li>', '').replace('<li>', '').replace('<u>', '').replace('</u>', '').\
                replace('&quot;', '').replace('</ul>', '').replace('<ul>', '')
            employer_url = data['site_url']
            employer_info.append({
                'name': name,
                'description': description,
                'employer_url': employer_url})
            if not employer_info:
                raise ValueError

            return employer_info

        except ValueError:
            raise ValueError('Ошибка данных.')

    def get_vacancies_from_api(self, employer_id: str) -> list[dict[str, Any]]:
        """ Метод для получения вакансий конкретного работодателя по его ID. """
        vacancies_url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        param = {
            'page': 0,
            'per_page': 100,
        }
        data = requests.get(url=vacancies_url, headers=HeadHunterAPI.headers, params=param, timeout=10).json()['items']

        vacancies_info = []
        try:
            for vacancy in data:
                if vacancy['salary']:
                    salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                    salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
                else:
                    salary_from = 0
                    salary_to = 0

                if vacancy['address']:
                    city = vacancy['address']['city']
                    street = vacancy['address']['street'] if vacancy['address']['street'] else ''
                    building = vacancy['address']['building'] if vacancy['address']['building'] else ''
                else:
                    city = ''
                    street = ''
                    building = ''

                address = f'{street} {building}'
                published = datetime.fromisoformat(vacancy['published_at']).strftime('%d-%m-%Y')
                responsibility = vacancy['snippet']['responsibility'] if vacancy['snippet']['responsibility'] else ''
                requirement = vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] else ''

                vacancies_info.append({
                    'vacancy_name': vacancy['name'],
                    'address': address,
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'published': published,
                    'vacancy_url': vacancy['alternate_url'],
                    'city': city,
                    'employment': vacancy['employment']['name'],
                    'requirement': requirement,
                    'responsibility': responsibility})

            if not vacancies_info:
                raise ValueError

            return vacancies_info

        except ValueError:
            raise ValueError('Ошибка данных.')
