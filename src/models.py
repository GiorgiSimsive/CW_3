"""
Модели для таблиц в базе данных PostgreSQL.
"""

CREATE_COMPANIES_TABLE = """
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    area VARCHAR(255),
    industry VARCHAR(255)
);
"""

CREATE_VACANCIES_TABLE = """
CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10),
    url TEXT
);
"""
