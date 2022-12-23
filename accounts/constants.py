from common.functions import ChoiceAdapter
from accounts.models import Contact


class ContactListBy(ChoiceAdapter):
    """Order by type for contacts"""
    ALL = 100
    INCOME = 200
    EXPENSE = 300


class ContactOrderBy(ChoiceAdapter):
    """Order by contact type"""
    LARGEST_AMOUNT = 100
    SMALLEST_AMOUNT = 200
    LARGEST_INCOME = 300
    SMALLEST_INCOME = 400
    LARGEST_EXPENSE = 500
    SMALLEST_EXPENSE = 600
    ALPHABETICAL = 700
    REVERSE_ALPABETICAL = 800
