from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from datetime import date, timezone
from django.conf import settings


# Create your models here.

class BaseModel(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, max_length=36, default=uuid4)
    created_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)


class PersonManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class Users(BaseModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(_("mobile_number"), max_length=10, unique=True)

    objects = PersonManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class EventInfo(BaseModel):
    name = models.CharField(_("name"), max_length=50)
    date = models.DateField()
    city = models.CharField(_("city"), max_length=50)
    rating = models.IntegerField(_("city member rating"), default=0)
    interested_user = models.IntegerField(_("interested user"), default=0)
