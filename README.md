# Проект: Вакансии HH и PostgreSQL

## Описание

Этот проект предназначен для получения данных о работодателях и их вакансиях с
сайта [hh.ru](https://hh.ru), сохранения этих данных в базе данных PostgreSQL, 
а также выполнения различных запросов к данным через специальный класс `DBManager`.

## Используемые технологии

- Python 3.10+
- PostgreSQL
- psycopg2
- requests
- hh.ru API

## Установка и запуск
1. Установите зависимости:
`pip install -r requirements.txt`
2. Создайте таблицы в PostgreSQL:
`python src/create_tables.py`
3. Запустите основной скрипт:
`python main.py`
