import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "lab0",
    "user": "postgres",
    "password": "postgres",
}


def show_tasks(cur, header):
    # ВИБІРКА: задачі разом з іменем відповідального (JOIN двох таблиць)
    cur.execute("""
        SELECT t.id, t.title, t.status, e.name
        FROM tasks t
        LEFT JOIN employees e ON e.id = t.employee_id
        ORDER BY t.id;
    """)
    print(f"\n--- {header} ---")
    for task_id, title, status, name in cur.fetchall():
        print(f"{task_id}. {title} | {status} | {name}")


with psycopg.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        show_tasks(cur, "Задачі на початку")

        # ЗМІНА: задача №1 тепер виконана
        cur.execute(
            "UPDATE tasks SET status = %s WHERE id = %s;",
            ("Зроблено", 1),
        )
        show_tasks(cur, "Після зміни статусу задачі №1")

        # ВИДАЛЕННЯ: видаляємо задачу №3
        cur.execute("DELETE FROM tasks WHERE id = %s;", (3,))
        show_tasks(cur, "Після видалення задачі №3")