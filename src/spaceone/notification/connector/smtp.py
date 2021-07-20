import smtplib
from email.mime.text import MIMEText
import logging

from spaceone.core.connector import BaseConnector
from spaceone.notification.conf.email_conf import *

__all__ = ['SMTPConnector']
_LOGGER = logging.getLogger(__name__)


class SMTPConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smtp = None

    def set_smtp(self, host, port, mail, password):
        self.smtp = smtplib.SMTP(host, port)
        self.smtp.starttls()
        self.smtp.login(mail, password)

    def send_email(self, to, subject, messages):
        msg = MIMEText(messages)
        msg['To'] = to
        msg['Subject'] = subject

        self.smtp.sendmail(SENDER_EMAIL_ADDR, to, msg.as_string())

        self.smtp.quit()
