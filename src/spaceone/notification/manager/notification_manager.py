from spaceone.core.manager import BaseManager
from spaceone.notification.manager.smtp_manager import SMTPManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, host, port, user, password, to, subject, messages, from_email):
        smtp_mgr: SMTPManager = self.locator.get_manager('SMTPManager')
        smtp_mgr.set_smtp(host, port, user, password)
        # smtp_mgr.request_send_email(to, subject, messages)
        smtp_mgr.request_send_email(to, subject, messages, from_email)
