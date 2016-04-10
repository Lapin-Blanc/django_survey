# -*- coding: utf-8 -*-
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(fromaddr, password, toaddr, subject, message):

    def _send_email(fromaddr, password, toaddr, subject, message):
        msg = MIMEMultipart('alternative')
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail("fromaddr", toaddr, text)
        server.quit()
    threading.Thread(
        target=_send_email,
        args=(fromaddr, password, toaddr, subject, message)
            ).start()
