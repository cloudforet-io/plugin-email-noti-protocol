import os
import logging
import datetime

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
                'title': '[Alerting] Alert 테스트',
                'link': 'https://google.com',
                'description': '서버 장애가 발생하였습니다. SpaceONE 에서 자세한 정보를 확인해 주세요. Thresholds Crossed: 1 out of the last 1 datapoints [0.6085129343340805 (17/08/21 12:41:00)] was less than the lower thresholds [0.3762805693896841] or greater than the upper thresholds [0.5195178482046605] (minimum 1 datapoint for OK -> ALARM transition).',
                'tags': [
                    {
                        'key': 'Alert Number',
                        'value': '#1111111'
                    },
                    {
                        'key': 'State',
                        'value': 'TRIGGERED'
                    },
                    {
                        'key': 'Urgency',
                        'value': 'HIGH'
                    },
                    {
                        'key': 'Project',
                        'value': 'Dev Project > 스페이스원 웹서버'
                    },
                    {
                        'key': 'Resource',
                        'value': 'server-yyyyy'
                    },
                    {
                        'key': 'Resource Name',
                        'value': 'web-server-001'
                    }
                ],
                'callbacks': [{
                    'label': 'Acknowledge',
                    'url': 'https://spaceone.console.doodle.spaceone.dev/monitoring/alert-system/alert/xxxxx'
                }],
                'occured_at': datetime.datetime.utcnow().isoformat()
            },
            'notification_type': 'ERROR',
            'secret_data': self.secret_data,
            'channel_data': self.channel_data
        })
