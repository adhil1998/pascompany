from django.db import models
from common.functions import encode
from django.conf import settings


# Create your models here.
class AbstractBaseModel(models.Model):
    """
    store common data fro all table
    """

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, null=True,
        blank=True, related_name="creator_%(class)s_objects",
        on_delete=models.SET_NULL)
    updater = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=None, null=True,
        blank=True, related_name="updater_%(class)s_objects",
        on_delete=models.SET_NULL)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the above model."""

        abstract = True
        ordering = ('-created_on',)

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)
