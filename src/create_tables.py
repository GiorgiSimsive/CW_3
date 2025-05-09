import psycopg2

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from src.models import CREATE_COMPANIES_TABLE, CREATE_VACANCIES_TABLE


def create_tables() -> None:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(CREATE_COMPANIES_TABLE)
    cur.execute(CREATE_VACANCIES_TABLE)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы.")
