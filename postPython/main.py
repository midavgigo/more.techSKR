import psycopg2 # либа связывающая питон и постргрес
from config import host, user, password, db_name

connection = None
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

# Создание таблицы в бд reviews
#    with connection.cursor() as cursor:
#        cursor.execute(
#            """CREATE TABLE BANKS(
#                id serial PRIMARY KEY,
#                description varchar(200) NOT NULL,
#                estimation varchar(5) NOT NULL
#            );"""
#        )

#        print("[INFO] Table created successfully")

# Вставляем отзывы в таблицу в наше бд
#    with connection.cursor() as cursor:
#        cursor.execute(
#            """INSERT INTO banks (description, estimation) VALUES
#            ('Good place', '10/10')"""
#        )
#
#        print("[INFO] Data was successfully iserted")

# вывод наших данных из таблицы
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM banks"""
        )

        print(cursor.fetchone())

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")