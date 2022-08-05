import os
import logging
from jinja2 import Environment, FileSystemLoader

from spaceone.core import utils
from spaceone.core.service import *
from spaceone.notification.manager.notification_manager import NotificationManager
from spaceone.notification.conf.email_conf import *
from spaceone.notification.error.custom import *


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
                    - link
                    - description
                    - short_description
                    - contents
                    - content_type
                    - image_url
                    - tags (list)
                        - key
                        - value
                        - options
                    - callbacks (list)
                        - url
                        - label
                        - options
                    - occurred_at
                - notification_type
                - secret_data:
                    - smtp_host
                    - smtp_port
                    - user
                    - password
                - channel_data
                    - email
        """

        secret_data = params.get('secret_data', {})
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']

        params_message = params['message']
        title = params_message['title']
        self._check_validate_message(params_message)
        contents = self.make_contents(params_message, notification_type)

        smtp_host = secret_data.get('smtp_host', DEFAULT_SMTP_SERVER)
        smtp_port = secret_data.get('smtp_port', DEFAULT_SMTP_PORT)
        user = secret_data.get('user', DEFAULT_SMTP_USER)
        password = secret_data.get('password', DEFAULT_SMTP_PASSWORD)

        email_list = channel_data.get('email')

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(smtp_host, smtp_port, user, password, email_list, title, contents)

    def make_contents(self, message, notification_type):
        env = Environment(loader=FileSystemLoader(searchpath="/"))

        template_kwargs = {
            'notification_type_color': self.get_notification_type_color(notification_type),
            'title': message.get('title', ''),
            'callbacks': message.get('callbacks', [])
        }

        if 'content_type' in message and message['content_type'] == 'HTML':
            template = env.get_template(self.get_html_template_path('notification_template_include_html_contents.html'))
            template_kwargs.update({
                'contents': message.get('contents', '')
            })
        else:
            template = env.get_template(self.get_html_template_path('notification_template.html'))
            template_kwargs.update({
                'description': message.get('description', ''),
                'tags': message.get('tags', [])
            })

            if 'image_url' in message:
                template_kwargs.update({'image_url': message['image_url']})

        if 'link' in message:
            template_kwargs.update({'link': message['link']})

        if 'occurred_at' in message:
            if occurred_at := self.convert_occurred_at(message['occurred_at']):
                template_kwargs.update({'occurred_at': occurred_at})

        return template.render(**template_kwargs)

    @staticmethod
    def _check_validate_message(message):
        if 'content_type' in message and message['content_type'] not in ['HTML', 'MARKDOWN']:
            raise ERROR_INVALID_MESSAGE(key='message.content_type', value=message['content_type'])

    @staticmethod
    def get_html_template_path(html_file_name):
        full_path = os.path.split(__file__)[0]
        split_dir = full_path.split('/')[:-1]
        split_dir.append('templates')
        split_dir[0] = '/'                     # root directory
        return os.path.join(*split_dir, html_file_name)

    @staticmethod
    def get_notification_type_color(notification_type):
        return NOTIFICATION_TYPE_COLOR_MAP.get(notification_type, NOTIFICATION_TYPE_DEFAULT_COLOR)

    @staticmethod
    def convert_occurred_at(occurred_at):
        if dt := utils.iso8601_to_datetime(occurred_at):
            return dt.strftime("%B %d, %Y %H:%M %p (UTC)")

        return None
