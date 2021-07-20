from spaceone.core.manager import BaseManager
from spaceone.notification.connector.smtp import SMTPConnector


class SMTPManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smtp_connector: SMTPConnector = self.locator.get_connector('SMTPConnector')

    def set_smtp(self, server, port, user, password):
        self.smtp_connector.set_smtp(server, port, user, password)

    def request_send_email(self, to, subject, messages):
        self.smtp_connector.send_email(to, subject, messages)
