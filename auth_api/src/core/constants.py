from enum import Enum


class DeviceTypes(Enum):
    PC = 'pc'
    MOBILE = 'mobile'
    OTHER = 'other'


DEVICES = [device.value for device in DeviceTypes]

PASSWORD_LEN = 6
PASSWORD_REGEX = r'[A-Za-z0-9@#$%^&+=]{6,}'
FAKE_MAIL_DOMAIN = '@fake.email'
