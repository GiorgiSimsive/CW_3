import psycopg2

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    def __init__(self) -> None:
        """
        Инициализация подключения к базе данных.
        """
        self.connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params: tuple | None = None) -> None:
        """
        Выполнение SQL-запроса.
        """
        self.cursor.execute(query, params)
        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получить список всех компаний и количество вакансий у каждой компании.
        """
        query = """
        SELECT companies.name, COUNT(vacancies.id)
        FROM companies
        LEFT JOIN vacancies ON companies.id = vacancies.company_id
        GROUP BY companies.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):  # type: ignore
        """
        Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты.
        """
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM vacancies
        JOIN companies ON companies.id = vacancies.company_id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получить среднюю зарплату по вакансиям.
        """
        query = """
        SELECT AVG((salary_min + salary_max) / 2) FROM vacancies;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]  # type: ignore

    def get_vacancies_with_higher_salary(self):  # type: ignore
        """
        Получить список вакансий с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM vacancies
        JOIN companies ON companies.id = vacancies.company_id
        WHERE (vacancies.salary_min + vacancies.salary_max) / 2 > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):  # type: ignore
        """
        Получить список вакансий, содержащих слово в названии.
        """
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary_min, vacancies.salary_max, vacancies.url
        FROM vacancies
        JOIN companies ON companies.id = vacancies.company_id
        WHERE vacancies.name ILIKE %s;
        """
        self.cursor.execute(query, ("%" + keyword + "%",))
        return self.cursor.fetchall()

    def insert_companies(self, employers: list):  # type: ignore
        """
        Вставляет данные о работодателях в таблицу companies.
        """
        for employer in employers:
            query = """
            INSERT INTO companies (id, name, area, industry)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            params = (employer["id"], employer["name"], employer["area"], employer["industry"])
            self.execute_query(query, params)

    def insert_vacancies(self, vacancies: list):  # type: ignore
        """
        Вставляет вакансии в таблицу vacancies.
        """
        for vacancy in vacancies:
            query = """
            INSERT INTO vacancies (company_id, name, salary_min, salary_max, salary_currency, url)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            params = (
                vacancy["company_id"],
                vacancy["name"],
                vacancy["salary_min"],
                vacancy["salary_max"],
                vacancy["salary_currency"],
                vacancy["url"],
            )
            self.execute_query(query, params)

    def close(self) -> None:
        """
        Закрыть соединение с БД.
        """
        self.cursor.close()
        self.connection.close()
