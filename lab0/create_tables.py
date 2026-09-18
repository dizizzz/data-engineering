import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "lab0",
    "user": "postgres",
    "password": "postgres",
}

SQL = """
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    id       SERIAL PRIMARY KEY,
    name     TEXT NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE tasks (
    id          SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('В процесі', 'Зроблено')),
    employee_id INTEGER REFERENCES employees(id) ON DELETE SET NULL
);
"""

with psycopg.connect(**DB_CONFIG) as conn:
    conn.execute(SQL)
    print("Таблиці employees і tasks створено.")