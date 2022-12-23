from common.functions import ChoiceAdapter
from accounts.models import Contact


class VTokenStatusChoices(ChoiceAdapter):
    VTOKEN_STATUS_UNUSED = 1
    VTOKEN_STATUS_USED = 2


class VTokenTypeChoices(ChoiceAdapter):
    VTOKEN_TYPE_SET_PASS = 1
    VTOKEN_TYPE_RESET_PASS = 2
    VTOKEN_TYPE_VERIFY_EMAIL = 3
    VTOKEN_TYPE_OTP = 4
    VTOKEN_TYPE_MAGIC = 5
    VTOKEN_TYPE_CHANGE_EMAIL = 6
    VTOKEN_STATUS_USED = 7
    VTOKEN_TYPE_VERIFY_EMAIL_OTP = 8
    VTOKEN_TYPE_RESET_PASS_OTP = 9

# Validity in Minutes
_10_MINUTES = 10 # 10 Minute
_30_MINUTES = 30  # 30 Minutes
_1_DAY = 1440  # 24 hours
_2_DAY = 2880  # 24 hours
_365_DAYS = 525600  # 365 days

TOKEN_VALIDITY = {
    VTokenTypeChoices.VTOKEN_TYPE_SET_PASS: _1_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS: _2_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL: _365_DAYS,
    VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL: _365_DAYS,
    VTokenTypeChoices.VTOKEN_TYPE_OTP: _30_MINUTES,
    VTokenTypeChoices.VTOKEN_TYPE_MAGIC: _2_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL_OTP: _2_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS_OTP: _10_MINUTES,
}

OTP_NOTIFICATIONS = [
    VTokenTypeChoices.VTOKEN_TYPE_OTP,
    VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL_OTP,
    VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS_OTP]