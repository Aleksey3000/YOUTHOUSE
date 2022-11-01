from flask import Flask, json, request, render_template, url_for
import SQL
import logging
from send_email import send_massage
from datetime import date
from info_halls import halls

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    halls[0]['url'] = url_for('static', filename='img/halls/Большой зал.jpg')
    halls[1]['url'] = url_for('static', filename='img/halls/Большой танцевальный зал.jpg')
    halls[2]['url'] = url_for('static', filename='img/halls/Бочки.jpg')
    halls[3]['url'] = url_for('static', filename='img/halls/Малый танцевальный зал.jpg')
    halls[4]['url'] = url_for('static', filename='img/halls/Ситцевая.jpg')

    hall = 'False'
    mydate = {'datenow': str(date.today())}

    if request.method == 'POST':
        if request.form.get('10') == '6':
            name = request.form.get('name')
            num = request.form.get('num')
            comp = request.form.get('comp')
            email = request.form.get('email')
            hall = request.form.get('hall')
            ev_name = request.form.get('ev_name')
            type1 = request.form.get('type')
            start = request.form.get('start')
            end = request.form.get('end')
            about = request.form.get('about')
            obor = (request.form.get('стул'), request.form.get('стол'), request.form.get('стол-журнальный'),
                    request.form.get('Телевизор'), request.form.get('диван'), request.form.get('стул-барный'),
                    request.form.get('колонки'), request.form.get('вешалка'), request.form.get('микшер'),
                    request.form.get('стойка-под-микро'))

            print(name, num, comp, email, hall, ev_name, type1, start, end, about, obor, sep=' - ')

            hall = 'False'

        else:
            num_hall = request.form.get('b')
            hall = halls[int(num_hall)]
    return render_template("index.html", halls=halls, hall=hall, date=mydate)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        b1 = request.form.get('b1')
        b2 = request.form.get('b2')
        print(b1, b2, type(b1))
    return render_template("comment.html")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    is_admin = False
    orders = []
    if request.method == 'POST':
        if request.form.get('button') == '0':
            username = request.form.get('log')
            password = request.form.get('pas')
            if username == 'admin' and password == '123':
                is_admin = True
                orders = SQL.all()
        else:
            rb = request.form.get('rb').split('-')
            comment = request.form.get('comment')
            info = SQL.select(int(rb[0]))
            if int(rb[1]):
                SQL.change_active(int(rb[0]), 'True')
                message = f'Здравствуйте, {info[1]}!\nВаша заявка на бронирование "{info[6]}" в областном центре культуры и молодежи (под номером {info[0]}) была одобрена!\nДата и время: с {info[4]} до {info[5]}\nМесто провeдения: г. Калининград, Московский проспект 60-62\nЕсли у вас возникнут вопросы по поводу проведения и организации мероприятий, вы можете задать их (на сайте qwe)\nЕсли вы хотите отказаться от бронирования, перейдите (по ссылке link2)\n\n\n\nС уважением, Администратор ОЦКМ admin_name.'
                send_massage('Ответ на поданную заявку.', message, info[2])
            else:
                message = f'Здравствуйте, {info[1]}!\nВаша заявка на бронирование "{info[6]}" в областном центре культуры и молодежи (под номером {info[0]}) была отменена.\nКомментарий:\n{comment}\n\n\n\nС уважением, Администратор ОЦКМ admin_name.'
                send_massage('Ответ на поданную заявку.', message, info[2])
            print(rb, type(rb))
            is_admin = True
            orders = SQL.all()

    return render_template("admin.html", is_admin=is_admin, orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
