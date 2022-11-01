import smtplib
from email.mime.text import MIMEText


def send_massage(theme, mes, client):
    sender = 'youth_house@mail.ru'
    password = '4VrnG2yX610Z3erT7Dzz'
    mes = MIMEText(mes)
    mes['Subject'] = theme  # ТЕМА
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    try:
        server.login(sender, password)
        server.sendmail(sender, client, mes.as_string())
        print('ALL RIGHT')
    except Exception as ex:
        print(f"ERROR: {ex}")
