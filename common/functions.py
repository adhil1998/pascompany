from hashids import Hashids
import enum
from random import randint

from django.conf import settings
from django.utils.timezone import localtime

from rest_framework.response import Response
from rest_framework import status

def encode(value):
    """
    Function to  hash hid the int value.

    Input Params:
        value(int): int value
    Returns:
        hashed string.
    """
    hasher = Hashids(
        min_length=5,
        salt='money_track')
    try:
        value = int(value)
        return hasher.encode(value)
    except:
        return None


def decode(value):
    """
    Function to  decode hash hid value.

    Input Params:
        value(str): str value
    Returns:
        int value.
    """
    hasher = Hashids(
        min_length=5,
        salt='money_track')
    try:
        return hasher.decode(value)[0]
    except:
        return None


class ChoiceAdapter(enum.IntEnum):
    @classmethod
    def choices(cls):
        return ((item.value, item.name.replace("_", " ")) for item in cls)


def _choiceadapter(enumtype):
    """Function to create choice filed in model from enum."""
    return (
        (item.value, item.name.replace('_', ' ').title()) for item in enumtype)


def success_response(data={}, message=None, status=status.HTTP_200_OK):
    """
    Function to create success Response.

    This function will create the standardized success response.
    """
    response = {
        'success': True,
        'detail': message,
        'code': status,
        'data': data
    }
    if not message:
        response['detail'] = 'Success.'
    return Response(response, status=status)

def generate_random_number(digits):
    """
    Function to generate n dig random number.

    Input Params:
        digits(int): number of digits
    Returns:
        (int): number
    """
    range_start = 10**(digits - 1)
    range_end = (10**digits) - 1
    return randint(range_start, range_end)


def date_time_desc(date):
    """Function to format date time."""
    try:
        date = localtime(date)
    except:
        pass
    date = date.strftime('%d %B %Y, %H:%M %p')
    date += ', Timezone: %s' % settings.TIME_ZONE
    return date