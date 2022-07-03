from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, max_length=36, default=uuid4)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(_('email address'), blank=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    password = models.CharField(_('password'), max_length=128)
    spam_count = models.IntegerField(default=0)

    REQUIRED_FIELDS = []

    objects = UserManager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def user_id(self):
        return self.id.__str__()
