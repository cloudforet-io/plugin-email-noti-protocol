import smtplib
import markdown
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from spaceone.core.connector import BaseConnector

__all__ = ['SMTPConnector']
_LOGGER = logging.getLogger(__name__)


class SMTPConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smtp = None

    def set_smtp(self, host, port, user, password):
        print(f'$$$ host: {host}, port: {port}, user: {user}, password: {password}')
        self.smtp = smtplib.SMTP(host, port)
        self.smtp.connect(host, port)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(user, password)

    def send_email(self, mail_list, subject, messages, from_email, mark_down=None):
        multipart_msg = MIMEMultipart("alternative")

        multipart_msg["Subject"] = subject
        multipart_msg["From"] = from_email
        multipart_msg["To"] = mail_list

        if mark_down:
            contents = markdown.markdown(mark_down)
        else:
            contents = messages

        multipart_msg.attach(MIMEText(contents, 'html'))

        self.smtp.sendmail(from_email, mail_list.split(','), multipart_msg.as_string())
        self.smtp.quit()
