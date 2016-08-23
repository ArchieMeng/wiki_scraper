import smtplib
from email.mime.text import MIMEText
import pickle

def send_mail(to,subject,text):
    f = open('passwd.p', 'r')

    mail_host = 'smtp-mail.outlook.com'
    mail_port = 587
    mail_name = 'myt1996037@hotmail.com'
    mail_pass = pickle.load(f)

    f.close()

    receiver = to

    message = MIMEText(text,'plain','utf-8')
    message['Subject'] = subject
    message['From'] = mail_name
    message['To'] = receiver

    smtpobj = smtplib.SMTP(mail_host,mail_port)
    print smtpobj.ehlo()
    print smtpobj.starttls()
    print smtpobj.login(mail_name,mail_pass)
    print smtpobj.sendmail(mail_name,[receiver],message.as_string())
    print smtpobj.quit()

if __name__ == '__main__':
    send_mail('506759765@qq.com','TEST','Hello!\nThis is a test email from Archie\n')



















