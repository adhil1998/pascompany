"""
This file is to convert id
"""
from django.conf import settings
from common.functions import decode, encode


class IDConverter:
    """
    Converter to convert encoded id in url to integer id
    """
    regex = '[0-9a-zA-Z]{%d,}' % 5

    def to_python(self, value):
        return decode(value)

    def to_url(self, value):
        return encode(value)