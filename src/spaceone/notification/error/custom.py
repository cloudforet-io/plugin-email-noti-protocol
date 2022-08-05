from spaceone.core.error import ERROR_BASE


class ERROR_INVALID_MESSAGE(ERROR_BASE):
    _message = 'Message is invalid. ({key}={value})'
