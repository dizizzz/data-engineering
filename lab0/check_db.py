import psycopg

# Підкл бази в Docker
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "lab0",
    "user": "postgres",
    "password": "postgres",
}

with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print("Підключення успішне!")
        print(version)