import psycopg2
import configSQL
from datetime import date, datetime

def sql(sql_command):
    class connection:
        pass

    setattr(connection, 'close', lambda: None)
    try:
        connection = psycopg2.connect(
            host=configSQL.HOST,
            port=configSQL.PORT,
            user=configSQL.USER,
            password=configSQL.PASSWORD,
            database=configSQL.DATABASE,
        )
        connection.autocommit = True
        print('Connected')
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            try:
                return cursor.fetchall()
            except:
                pass

    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        print('Closed')


def create_table():
    sql("CREATE TABLE info (id serial PRIMARY KEY, name TEXT NOT NULL, email varchar(255) NOT NULL, "
        "company TEXT NOT NULL, begin_date timestamp NOT NULL, end_date timestamp NOT NULL,"
        "hall varchar(27) NOT NULL, event_name TEXT NOT NULL, event_type varchar(16) NOT NULL, device TEXT NOT NULL, "
        "event_describe TEXT NOT NULL, furniture TEXT NOT NULL, phone_number varchar(13) NOT NULL, "
        "is_active BOOLEAN)")


def create(b_date, e_date, hall, ev_name, ev_type, ev_describe, device, furn, name, comp, email, mob_ph, is_active):
    sql(f"INSERT INTO info (name, email, company, begin_date, end_date, hall, event_name, "
        f"device, event_type ,event_describe, furniture, phone_number, is_active)"
        f"VALUES ('{name}', '{email}', '{comp}', '{b_date}', '{e_date}', '{hall}', '{ev_name}', "
        f"'{device}', '{ev_type}', '{ev_describe}', '{furn}', '{mob_ph}', '{is_active}')")
    print('Successfully create requests!')


def all():
    return sql(f"SELECT * FROM info")


def select(id_info):
    return sql(f"SELECT * FROM info WHERE id = {id_info}")[0]


def del_comment(id_comment):
    sql(f"DELETE FROM comments WHERE id = '{id_comment}'")


def change_active(id, value):
    sql(f"UPDATE info SET is_active = {value} WHERE id = {id}")


if __name__ == '__main__':
    sql("UPDATE info SET is_active = False WHERE is_active = True")
    [print(i) for i in sql('SELECT * FROM info')]
    #print(select(2))
