import os
import logging

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

SMTP_HOST = os.environ.get('SMTP_HOST', None)
SMTP_PORT = os.environ.get('SMTP_PORT', None)
SMTP_USER = os.environ.get('SMTP_USER', None)
SMTP_PW = os.environ.get('SMTP_PW', None)


class TestVoiceCallNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'smtp_host': SMTP_HOST,
        'smtp_port': SMTP_PORT,
        'user': SMTP_USER,
        'password': SMTP_PW
    }
    channel_data = {
        'email_list': [
            'abc@localhost'
        ],
    }

    def test_init(self):
        v_info = self.notification.Protocol.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify({'options': options, 'secret_data': self.secret_data})

    def test_dispatch(self):
        options = {}

        self.notification.Notification.dispatch({
            'options': options,
            'message': {
                'title': 'Alert 테스트',
                'description': '서버 장애가 발생하였습니다. SpaceONE 에서 자세한 정보를 확인해 주세요.',
                'tags': [
                    {
                        'key': 'project_id',
                        'value': 'project-xxxxx'
                    },
                    {
                        'key': 'project_name',
                        'value': '스페이스원 웹서버'
                    },
                    {
                        'key': 'resource_id',
                        'value': 'server-yyyyy'
                    },
                    {
                        'key': 'resource_name',
                        'value': 'web-server-001'
                    }
                ],
                'callbacks': [{
                    'url': 'https://spaceone.console.doodle.spaceone.dev/monitoring/alert-system/alert/xxxxx'
                }
                ]
            },
            'notification_type': 'ERROR',
            'secret_data': self.secret_data,
            'channel_data': self.channel_data
        })
