from src.create_tables import create_tables
from src.data_fetcher import DataFetcher
from src.db_manager import DBManager
from src.utils import fill_tables

companies = [
    {"id": "1740", "name": "Яндекс"},
    {"id": "3529", "name": "СБЕР"},
    {"id": "2180", "name": "Ozon"},
    {"id": "80", "name": "Альфа-Банк"},
    {"id": "15478", "name": "VK"},
    {"id": "78638", "name": "Т-Банк"},
    {"id": "1122462", "name": "Skyeng"},
    {"id": "5331842", "name": "Самокат (ООО Лидер консалт - официальный партнер)"},
    {"id": "3776", "name": "МТС"},
    {"id": "54979", "name": "АШАН Ритейл Россия"},
]


if __name__ == "__main__":
    print("Создание таблиц...")
    create_tables()

    fetcher = DataFetcher(companies)
    employers = fetcher.fetch_employers()
    vacancies = fetcher.fetch_vacancies()

    print("Загрузка данных...")
    fill_tables(employers, vacancies)

    db = DBManager()

    print("\nМеню:")
    print("1 - Компании и количество вакансий")
    print("2 - Все вакансии")
    print("3 - Средняя зарплата")
    print("4 - Вакансии с ЗП выше средней")
    print("5 - Поиск по ключевому слову")
    print("0 - Выход")

    while True:
        choice = input("\nВыбор: ")
        if choice == "1":
            for row in db.get_companies_and_vacancies_count():
                print(row)
        elif choice == "2":
            for row in db.get_all_vacancies():
                print(row)
        elif choice == "3":
            print("Средняя зарплата:", db.get_avg_salary())
        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(row)
        elif choice == "5":
            keyword = input("Ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(row)
        elif choice == "0":
            db.close()
            print("Выход.")
            break
        else:
            print("Неверный ввод.")
