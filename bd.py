import psycopg2

def create_db_structure():
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL,
                    phone_number TEXT NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            """)

def add_client(first_name, last_name, email):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s)", (first_name, last_name, email))

def add_phone(client_id, phone_number):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phones (client_id, phone_number) VALUES (%s, %s)", (client_id, phone_number))

def update_client(client_id, first_name=None, last_name=None, email=None):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE clients SET first_name = COALESCE(%s, first_name), last_name = COALESCE(%s, last_name), email = COALESCE(%s, email) WHERE id = %s", (first_name, last_name, email, client_id))

def delete_phone(phone_id):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phones WHERE id = %s", (phone_id,))

def delete_client(client_id):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phones WHERE client_id = %s", (client_id,))
            cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))

def find_client(first_name='%', last_name='%', email='%', phone_number='%'):
    with psycopg2.connect("dbname=clients_db user=postgres password=your_password") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.first_name, c.last_name, c.email, p.phone_number
                FROM clients c
                LEFT JOIN phones p ON c.id = p.client_id
                WHERE c.first_name LIKE %s
                  AND c.last_name LIKE %s
                  AND c.email LIKE %s
                  AND p.phone_number LIKE %s
            """, (first_name, last_name, email, phone_number))
            result = cur.fetchall()
    return result


if __name__ == "__main__":
    # Создание структуры БД
    create_db_structure()

    # Добавление новых клиентов
    add_client("Иван", "Иванов", "ivan@example.com")
    add_client("Петр", "Петров", "petr@example.com")
    add_client("Мария", "Сидорова", "maria@example.com")

    # Добавление телефонов для клиентов
    add_phone(1, "+79001112233")
    add_phone(1, "+79004445566")
    add_phone(2, "+79007778899")

    # Изменение данных о клиенте
    update_client(1, first_name="Иван", last_name="Новый", email="ivan_new@example.com")

    # Удаление телефона для клиента
    delete_phone(2)

    # Удаление клиента
    delete_client(3)

    # Поиск клиентов
    print(find_client(first_name="Иван"))
    print(find_client(last_name="Петр"))
    print(find_client(phone_number="9001112233"))