import logging

from spaceone.core.service import *
from spaceone.core.utils import parse_endpoint
from spaceone.notification.manager.notification_manager import NotificationManager
from spaceone.notification.conf.email_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'message', 'notification_type'])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message
                    - title
                    - markdown
                    - description
                    - tags (list)
                        - key
                        - value
                        - options
                    - callbacks (list)
                        - url
                        - options
                - notification_type
                - secret_data:
                    - smtp_host
                    - smtp_port
                    - user
                    - password
                - channel_data
                    - email_list
        """

        secret_data = params.get('secret_data', {})
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']

        params_message = params['message']
        title = params_message['title']
        contents = self.make_contents(params_message, notification_type)

        smtp_host = secret_data.get('smtp_host', DEFAULT_SMTP_SERVER)
        smtp_port = secret_data.get('smtp_port', DEFAULT_SMTP_PORT)
        user = secret_data.get('user', DEFAULT_SMTP_USER)
        password = secret_data.get('password', DEFAULT_SMTP_PASSWORD)

        email_list = channel_data.get('email_list')

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(smtp_host, smtp_port, user, password, email_list, title, contents)

    def make_contents(self, message, notification_type):
        markdown_text = f'# {message["title"]}\n' \
                        f'## Notification Type: {notification_type}\n' \
                        f'{message["description"]}\n'

        for tag in message.get('tags', []):
            markdown_text = f'{markdown_text}\n' \
                            f'* {tag["key"]}: {tag["value"]}\n'

        return markdown_text
