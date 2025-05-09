import requests

from config.config import HH_API_URL


class DataFetcher:
    """
    Класс для получения данных о компаниях и вакансиях с API hh.ru.
    """

    def __init__(self, companies: list):
        self.companies = companies

    def fetch_employers(self) -> list:
        """
        Получает подробную информацию о компаниях.
        :return: список словарей с данными о работодателях.
        """
        employers = []
        for company in self.companies:
            url = f"https://api.hh.ru/employers/{company['id']}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                employers.append(
                    {
                        "id": int(data["id"]),
                        "name": data["name"],
                        "area": data.get("area", {}).get("name"),
                        "industry": data.get("industries", [{}])[0].get("name"),
                    }
                )
        return employers

    def fetch_vacancies(self) -> list:
        """
        Получает все вакансии для заданного списка компаний.
        :return: список словарей с вакансиями.
        """
        all_vacancies = []
        for company in self.companies:
            print(f"Загружаем вакансии для компании: {company['name']}")
            page = 0
            while True:
                url = f"{HH_API_URL}?employer_id={company['id']}&page={page}&per_page=100"
                response = requests.get(url)
                if response.status_code != 200:
                    print(f"Ошибка запроса для {company['name']}: {response.status_code}")
                    break

                data = response.json()
                items = data.get("items", [])
                for vacancy in items:
                    salary = vacancy.get("salary") or {}
                    all_vacancies.append(
                        {
                            "company_id": int(company["id"]),
                            "name": vacancy["name"],
                            "salary_min": salary.get("from"),
                            "salary_max": salary.get("to"),
                            "salary_currency": salary.get("currency"),
                            "url": vacancy["alternate_url"],
                        }
                    )

                if page >= data.get("pages", 0) - 1:
                    break
                page += 1
        return all_vacancies
