from os import getenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from smtplib import SMTP_SSL
from models import User


def build_www_link(path):
    return getenv("WWW_HOST") + path


def send_email(email_to, subject, body):
    msg = MIMEMultipart()

    msg['From'] = getenv("SMTP_FROM")
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    ssl_context = ssl.create_default_context()
    smtp_server = SMTP_SSL(getenv("SMTP_HOST"), getenv(
        "SMTP_PORT"), context=ssl_context)

    smtp_server.login(getenv("SMTP_USER"), getenv("SMTP_PASS"))

    smtp_server.sendmail(msg['From'], email_to, msg.as_string())
    smtp_server.quit()
