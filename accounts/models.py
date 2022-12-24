from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from accounts import constants as acc_constants
from common.functions import encode, decode, generate_random_number, date_time_desc
from common.models import AbstractBaseModel
from django.utils.crypto import get_random_string


# Create your models here.

class User(AbstractUser):
    """ User model """
    phone_number = models.CharField(
        max_length=15, default=0, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    aadhar = models.URLField(null=True, blank=True)
    type = models.IntegerField(
        default=acc_constants.UserTypeChoices.SALESMAN,
        choices=acc_constants.UserTypeChoices.choices())

    def __str__(self):
        return f'{self.username} {self.idencode}'

    @property
    def idencode(self):
        """Return converted id"""
        return encode(self.id)

    def logout(self):
        """Logout user"""
        try:
            token = AccessToken.objects.get(user=self)
            token.refresh()
        except:
            pass

    def issue_access_token(self):
        """Function to get or create user access token."""
        token, created = AccessToken.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()
        return token.key


class AccessToken(models.Model):
    """To create and store bearer token"""
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    key = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.key:
            self.key = get_random_string(90)
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = get_random_string(90)
        if AccessToken.objects.filter(key=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.key = self.generate_unique_key()
        self.save()


class ValidationToken(AbstractBaseModel):
    """
    Class to store the validation token data.

    This is a generic model to store and validate all
    sort of tokens including password setters, one time
    passwords and email validations
    Attribs:
        user(obj): user object
        req_browser(str): browser of the user requested.
        req_location(str): location of the request created.
        set_browser(str): browser of the user updated.
        set_location(str): location of the request updated.
        key (str): token.
        status(int): status of the validation token
        expiry(datetime): time up to which link is valid.
        type(int): type indicating the event associated.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_info = models.JSONField(default=dict, null=True, blank=True,
                                verbose_name='additional_info')

    key = models.CharField(
        default='', max_length=200, blank=True)
    status = models.IntegerField(
        default=acc_constants.VTokenStatusChoices.VTOKEN_STATUS_UNUSED,
        choices=acc_constants.VTokenStatusChoices.choices())
    expiry = models.DateTimeField(default=timezone.now)
    type = models.IntegerField(
        default=0, choices=acc_constants.VTokenTypeChoices.choices())

    def __str__(self):
        """Object name in django admin."""
        return str(self.user.name) + ': ' + str(self.key) + ":  " + str(
            self.id)

    def save(self, *args, **kwargs):
        """
        Overriding the default save signal.

        This function will generate the token key based on the
        type of the token and save when the save() function
        is called if the key is empty. It. will. also set the
        expiry when the object is created for the first time.
        """
        if not self.key:
            self.key = self.generate_unique_key()
        if not self.id:
            self.expiry = self.get_expiry()
        return super(ValidationToken, self).save(*args, **kwargs)

    def get_validity_period(self):
        return acc_constants.TOKEN_VALIDITY[self.type]

    def get_expiry(self):
        """Function to get the validity based on type."""
        validity = self.get_validity_period()
        return (timezone.now() + timedelta(
            minutes=validity))

    def generate_unique_key(self):
        """Function to generate unique key."""
        if self.type not in acc_constants.OTP_NOTIFICATIONS:
            key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        else:
            key = generate_random_number(settings.OTP_LENGTH)

        if ValidationToken.objects.filter(
                key=key, type=self.type,
                status=acc_constants.VTokenStatusChoices.VTOKEN_STATUS_UNUSED).exists():
            key = self.generate_unique_key()
        return key

    def validate(self):
        """Function to. validate the token."""
        status = True
        if not self.is_valid:
            status = False
        self.status = acc_constants.VTokenStatusChoices.VTOKEN_STATUS_USED
        self.updater = self.user
        self.save()
        return status

    def refresh(self):
        """Function  to refresh the validation token."""
        if not self.is_valid:
            self.key = self.generate_unique_key()
            self.status = acc_constants.VTokenStatusChoices.VTOKEN_STATUS_UNUSED
        self.expiry = self.get_expiry()
        self.updater = self.user
        self.save()
        return True

    def mark_as_used(self):
        """ Function to mark validation token as used """
        self.status = acc_constants.VTokenStatusChoices.VTOKEN_STATUS_USED
        self.save()

    @staticmethod
    def initialize(user, type, creator=None):
        """Function to initialize verification."""
        validation, created = ValidationToken.objects.get_or_create(
            user=user, type=type, creator=creator,
            status=acc_constants.VTokenStatusChoices.VTOKEN_STATUS_UNUSED)
        if not created:
            validation.refresh()
        return validation.notify()

    @property
    def validity(self):
        """Function to get the validity of token."""
        return date_time_desc(self.expiry)

    @property
    def created_on_desc(self):
        """Function to get the validity of token."""
        return date_time_desc(self.created_on)

    @property
    def is_valid(self):
        """Function  which check if Validator is valid."""
        if self.expiry > timezone.now() and (
                self.status == acc_constants.VTokenStatusChoices.VTOKEN_STATUS_UNUSED):
            return True
        return False
