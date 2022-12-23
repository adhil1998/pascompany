from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from common.functions import encode, decode
from common.models import AbstractBaseModel
from django.utils.crypto import get_random_string


# Create your models here.

class User(AbstractUser):
    """ User model """
    phone_number = models.CharField(max_length=15, default=0, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)

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


class Contact(AbstractBaseModel):
    """M0del to create data of contacts"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.idencode}'
