from uuid import uuid4

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models, transaction
from django.db.models import SET_NULL
from django.utils.translation import ugettext as _

IdField = models.UUIDField(primary_key=True, default=uuid4, editable=False)
tweet_length = 140


class Reply(models.Model):
    id = IdField
    # Business Rule: Replies must be deleted on user delete method, so this models needs to be before "User".
    # Since "Occurrence" model doesn't exist yet, it can be referenced by a string.
    occurrence = models.ForeignKey('Occurrence', related_name='replies')
    message = models.CharField(max_length=tweet_length)


class User(AbstractBaseUser):
    id = IdField
    name = models.CharField(_('Name'), max_length=80)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'

    @transaction.atomic
    def delete(self, **kwargs):
        Reply.objects.filter(occurrence__vehicle__owner=self).distinct().delete()
        return super(User, self).delete(**kwargs)

    def get_full_name(self):  # "Interface" method
        raise NotImplementedError(settings.MESSAGES['NOT_IMPLEMENTED'])

    def get_short_name(self):  # "Interface" method
        raise NotImplementedError(settings.MESSAGES['NOT_IMPLEMENTED'])


class Vehicle(models.Model):
    id = IdField
    owner = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name='vehicles')
    license_plate = models.CharField(_('License Plate'), max_length=8, unique=True)
    color = models.CharField(_('Color'), max_length=20, null=True)
    model = models.CharField(_('Model'), max_length=40, null=True)
    brand = models.CharField(_('Brand'), max_length=40, null=True)

    def delete(self, *args, **kwargs):
        raise NotImplementedError(settings.MESSAGES['NOT_IMPLEMENTED'])


class Occurrence(models.Model):
    id = IdField
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL, related_name='occurrences')
    vehicle = models.ForeignKey(Vehicle, related_name='occurrences')
    description = models.CharField(max_length=tweet_length)
    date_time = models.DateTimeField(auto_now_add=True, editable=False)

    def delete(self, *args, **kwargs):
        raise NotImplementedError(settings.MESSAGES['NOT_IMPLEMENTED'])
