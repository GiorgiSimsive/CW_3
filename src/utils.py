from typing import Any, Dict, List

import psycopg2

from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def fill_tables(employers: List[Dict[str, Any]], vacancies: List[Dict[str, Any]]) -> None:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()

    for employer in employers:
        cur.execute(
            """
            INSERT INTO companies (id, name, area, industry)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """,
            (employer["id"], employer["name"], employer["area"], employer["industry"]),
        )

    for vacancy in vacancies:
        cur.execute(
            """
            INSERT INTO vacancies (company_id, name, salary_min, salary_max, salary_currency, url)
            VALUES (%s, %s, %s, %s, %s, %s);
        """,
            (
                vacancy["company_id"],
                vacancy["name"],
                vacancy["salary_min"],
                vacancy["salary_max"],
                vacancy["salary_currency"],
                vacancy["url"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Данные успешно загружены.")
