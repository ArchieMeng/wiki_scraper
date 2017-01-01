import smtplib
from email.mime.text import MIMEText
import pickle
from makeEmailFile import makeEmailFile


def send_mail(to,subject,text):
    mail_data = get_mail_data()

    if mail_data:
        receiver = to

        message = MIMEText(text,'plain','utf-8')
        message['Subject'] = subject
        message['From'] = mail_data['mail_name']
        message['To'] = receiver

        smtpobj = smtplib.SMTP(mail_data['mail_host'], int(mail_data['mail_port']))
        print smtpobj.ehlo()
        print smtpobj.starttls()
        print smtpobj.login(mail_data['mail_name'], mail_data['mail_pass'])
        print smtpobj.sendmail(mail_data['mail_name'], [receiver], message.as_string())
        print smtpobj.quit()


def get_mail_data():
    try:
        f = open('mail_data.p', 'r')
        mail_data = pickle.load(f)
        f.close()
        return mail_data
    except IOError:
        makeEmailFile()
        return get_mail_data()


if __name__ == '__main__':
    receiver = raw_input("input your email address:\t")
    send_mail(receiver, 'TEST', 'Hello!\nThis is a test email from {0}\n'
              .format(get_mail_data()['mail_name']))



















