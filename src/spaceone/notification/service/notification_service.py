import os
import logging
import time
from jinja2 import Environment, FileSystemLoader

from spaceone.core import utils
from spaceone.core.service import *
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
                        - label
                        - options
                    - occured_at
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
        env = Environment(loader=FileSystemLoader(searchpath="./"))
        template = env.get_template(self.get_html_template_path())

        template_kargs = {
            'notification_type_color': self.get_notification_type_color(notification_type),
            'title': message.get('title', ''),
            'description': message.get('description', ''),
            'tags': message.get('tags', []),
            'callbacks': message.get('callbacks', [])
        }

        if 'link' in message:
            template_kargs.update({
                'link': message['link']
            })

        if 'occured_at' in message:
            if occured_at := self.convert_occured_at(message['occured_at']):
                template_kargs.update({
                    'occured_at': occured_at
                })

        return template.render(**template_kargs)

    @staticmethod
    def get_html_template_path():
        full_path = os.path.split(__file__)[0]
        split_dir = full_path.split('/')[:-1]
        split_dir.append('templates')

        return os.path.join(*split_dir, 'notification_template.html')

    @staticmethod
    def get_notification_type_color(notification_type):
        return NOTIFICATION_TYPE_COLOR_MAP.get(notification_type, NOTIFICATION_TYPE_DEFAULT_COLOR)

    @staticmethod
    def convert_occured_at(occured_at):
        if dt := utils.iso8601_to_datetime(occured_at):
            return dt.strftime("%B %d, %Y %H:%M %p (UTC)")

        return None
