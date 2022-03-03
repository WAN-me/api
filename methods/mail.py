import smtplib
import cfg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(mail, content, subject="", advanced=""):

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)

        smtpObj.login(cfg.mail_admin_user, cfg.mail_admin_pass)
        html = content
        to = mail

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = to
        msg.attach(MIMEText(html, 'html'))
        msg.attach(MIMEText(advanced, 'plain'))

        smtpObj.sendmail(cfg.mail_admin_user, to, msg.as_string())
        smtpObj.quit()

        return True
    except BaseException:
        return False


if __name__ == "__main__":
    send("wex335@yandex.ru", '''Hello, world''')
