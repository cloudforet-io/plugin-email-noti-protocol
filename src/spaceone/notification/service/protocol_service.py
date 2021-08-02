import logging
from spaceone.core.service import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class ProtocolService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return {'metadata': {
            'data_type': 'PLAIN_TEXT',
            'data': {
                'schema': {
                    'properties': {
                        'email': {
                            'description': 'Email address to receive notifications',
                            'minLength': 10,
                            'title': 'Email Address',
                            'type': 'string',
                            'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$',
                            'examples': ['user1@test.com']
                        }
                    },
                    'required': [
                        'email'
                    ],
                    'type': 'object'
                }
            }
        }}

    @transaction
    @check_required(['options'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        return {}
