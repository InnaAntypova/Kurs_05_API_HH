from abc import ABC, abstractmethod


class ABCApi(ABC):
    """ Абстрактный класс для получения данных от API. """

    @abstractmethod
    def get_employer_id_from_api(self, text: str):
        """ Метод для получения ID работодателя по текстовому названию компании от API. """
        pass

    @abstractmethod
    def get_employer_info_from_api(self, employer_id: str):
        """ Метод для получения информации о работодателе по его ID. """
        pass

    @abstractmethod
    def get_vacancies_from_api(self, employer_id: str):
        """ Метод для получения вакансий конкретного работодателя по его ID. """
        pass

