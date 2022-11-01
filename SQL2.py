import psycopg2
import configSQL
import datetime
from send_email import send_massage


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


def create_table():
    sql("CREATE TABLE info (id serial PRIMARY KEY, name TEXT NOT NULL, email varchar(255) NOT NULL, "
        "company TEXT NOT NULL, begin_date timestamp NOT NULL, end_date timestamp NOT NULL,"
        "hall varchar(27) NOT NULL, event_name TEXT NOT NULL, event_type varchar(16) NOT NULL, device TEXT NOT NULL, "
        "event_describe TEXT NOT NULL, furniture TEXT NOT NULL, phone_number varchar(13) NOT NULL, "
        "is_active BOOLEAN)")


def create_comment(name, email, text, date):
    sql(f"INSERT INTO comments (name, email, text, date) VALUES ('{name}', '{email}', '{text}', '{date}')")


def select_comments():
    my_list = []
    result_list = sql(f"SELECT * FROM comments")
    for i in result_list:
        my_dict = dict()
        my_dict['name'] = i[1]
        my_dict['email'] = i[2]
        my_dict['text'] = i[3]
        my_dict['date'] = i[4]
        my_list.append(my_dict)
    return my_list


def del_comment(id_comment):
    sql(f"DELETE FROM comments WHERE id = '{id_comment}'")


def change_active(id_comment, value):
    sql(f"UPDATE comments SET is_active = '{value}' WHERE name = '{id_comment}'")


def create(b_date, e_date, hall, ev_name, ev_type, ev_describe, device, furn, name, comp, email, mob_ph, is_active):
    sql(f"INSERT INTO info (name, email, company, begin_date, end_date, hall, event_name, "
        f"device, event_type ,event_describe, furniture, phone_number, is_active)"
        f"VALUES ('{name}', '{email}', '{comp}', '{b_date}', '{e_date}', '{hall}', '{ev_name}', "
        f"'{device}', '{ev_type}', '{ev_describe}', '{furn}', '{mob_ph}', '{is_active}')")
    print('Successfully create requests!')


def transform(date, ymd=False, dtm=False):
    if ymd:
        norm_data = list(map(int, str(date)[:10].split('-')))
        return norm_data
    elif dtm:
        norm_data = list(map(int, str(date)[11:19].split(':')))
        return norm_data
    else:
        return list(str(date)[:19].split())


def trans(begin_date, end_date):
    with open('datum_point.txt', 'r', encoding='utf-8') as file:
        datum_point = file.read()
    now_data = transform(datum_point, ymd=True)
    now_time = transform(datum_point, dtm=True)
    month_b = transform(begin_date[:19], ymd=True)[1] - now_data[1]
    if month_b:
        days_b = transform(begin_date[:19], ymd=True)[2] + 30 * month_b - now_data[2] + 1
    else:
        days_b = transform(begin_date[:19], ymd=True)[2] - now_data[2]
    if days_b:
        hours_b = transform(begin_date[:19], dtm=True)[0] + days_b * 24 - now_time[0] + 1
    else:
        hours_b = transform(begin_date[:19], dtm=True)[0] - now_time[0]
    if hours_b:
        minutes_b = transform(begin_date[:19], dtm=True)[1] + hours_b * 60 - now_time[1] + 1
    else:
        minutes_b = transform(begin_date[:19], dtm=True)[1] - now_time[1]
    month_e = transform(end_date[:19], ymd=True)[1] - now_data[1]
    if month_e:
        days_e = transform(end_date[:19], ymd=True)[2] + 30 * month_e - now_data[2] + 1
    else:
        days_e = transform(end_date[:19], ymd=True)[2] - now_data[2]
    if days_e:
        hours_e = transform(end_date[:19], dtm=True)[0] + days_e * 24 - now_time[0] + 1
    else:
        hours_e = transform(end_date[:19], dtm=True)[0] - now_time[0]
    if hours_e:
        minutes_e = transform(end_date[:19], dtm=True)[1] + hours_e * 60 - now_time[1] + 1
    else:
        minutes_e = transform(end_date[:19], dtm=True)[1] - now_time[1]

    return [minutes_b, minutes_e]


def check(begin_date, end_date, hall_us):
    k = 0
    hal = hall_us
    minutes_b, minutes_e = trans(begin_date, end_date)[0], trans(begin_date, end_date)[1]
    try:
        for i, j, q in sql('SELECT begin_date, end_date, hall FROM info'):
            begin_time_bd = trans(str(i), str(j))[0]
            end_time_bd = trans(str(i), str(j))[1]
            if begin_time_bd <= minutes_b <= end_time_bd and \
                    begin_time_bd <= minutes_e <= end_time_bd and q == hall:
                k += 1
        if k == 0:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return True


cr_begin_data = '2022-12-08 10:30:00'
cr_end_data = '2022-12-09 19:30:00'
cr_hall = 'Ситцевая'
cr_ev_name = 'Рисование - наше всё!'
cr_ev_type = 'Развлекательный'
cr_ev_describe = 'Откроете замочек к своему скрытому таланту!'
cr_device = 'Ничего'
cr_furn = 'Ничего'
cr_name = 'Вычужин Кирилл Андреевич'
cr_comp = 'МБОУ СОШ г.Пионерского'
cr_email = 'shprotakerill@gmail.com'
cr_mob_ph = '+79520532838'
cr_is_active = True
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(cr_begin_data + '  ')
    f.write(cr_end_data + '  ')
    f.write(cr_hall + '  ')
    f.write(cr_ev_name + '  ')
    f.write(cr_ev_type + '  ')
    f.write(cr_ev_describe + '  ')
    f.write(cr_device + '  ')
    f.write(cr_furn + '  ')
    f.write(cr_name + '  ')
    f.write(cr_comp + '  ')
    f.write(cr_email + '  ')
    f.write(cr_mob_ph + '  ')
    f.write(str(cr_is_active))
with open('file.txt', 'r', encoding='utf-8') as f:
    a = f.read()
a = a.split('  ')
beg_date = a[0]
end_date = a[1]
hall = a[2]
ev_name = a[3]
ev_type = a[4]
ev_describe = a[5]
device = a[6]
furn = a[7]
name = a[8]
comp = a[9]
email = a[10]
mob_ph = a[11]
is_active = a[12]

if is_active == "False":
    is_active = False

if __name__ == '__main__':
    #create(beg_date, end_date, hall, ev_name, ev_type, ev_describe, device, furn, name, comp, email, mob_ph, is_active)
    for i in sql('SELECT * FROM info'):
        print(i)
    if check(beg_date, end_date, hall):
        sq = sql('SELECT name, hall, begin_date, end_date, email, id FROM info WHERE is_active = True')
        for i in sq:
            name = i[0]
            room = i[1]
            beg_data = i[2]
            end_data = i[3]
            email = i[4]
            id = i[5]
            msg = f'Здравствуйте, {name}!\nВы подали заявку на бронирование зала {room} в период с {beg_data} по {end_data}.\nНомер вашей заявки: {id}.\nПо вопросам пишите на нашу почту: тут должна быть почта'
            Send.send_massage('Информация о заявке.', msg, email)
            if sq:
                for i in sq:
                    print(i)
                    name = i[0]
                    room = i[1]
                    beg_data = i[2]
                    end_data = i[3]
                    email = i[4]
                    id = i[5]
                    message_good = f'Здравствуйте, {name}!\nВаша заявка на бронирование "{room}" в областном центре культуры и молодежи (под номером {id}) была одобрена!\nДата и время: с {beg_data} до {end_data}\nМесто провeдения: г. Калининград, Московский проспект 60-62\nЕсли у вас возникнут вопросы по поводу проведения и организации мероприятий, вы можете задать их (на сайте qwe)\nЕсли вы хотите отказаться от бронирования, перейдите (по ссылке link2)\n\n\n\nС уважением, Администратор ОЦКМ admin_name.'
                    sender.send_massage('Ответ на поданную заявку.', message_good, email)
            else:
                sq = sql('SELECT name, hall, begin_date, end_date, email FROM info WHERE is_active = true')
                for i in sq:
                    name = i[0]
                    room = i[1]
                    beg_data = i[2]
                    end_data = i[3]
                    email = i[4]
                    id = i[5]
                    prichina = 'Потому что'
                    message_bad = f'Здравствуйте, {name}!\nВаша заявка на бронирование {room} в областном центре культуры и молодежи (под номером {id}) к сожалению была отклонена.\nПричина отказа "{prichina}"\nПовторно подать заявку  можно на (сайте link3)'
                    sender.send_massage('Ответ на поданную заявку.', message_bad, email)
