import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from account.help import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not username:
            raise ValueError("username not exists")
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(BaseModel, AbstractBaseUser):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        help_text=_("Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"unique": _("A user with that username already exists.")},
    )

    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.CharField(_("email address"), null=True, max_length=50)
    phone_number = models.CharField(
        _("Phone Number"), max_length=15, null=True, blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    blob = JSONField(_("Blob"), blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def short_name(self):
        return self.first_name

    def get_username(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def __str__(self):
        return self.get_username()

    def user_id(self):
        return self.id.__str__()

class Session(BaseModel):
    session_id = models.CharField(max_length=32,unique=True)
    user = models.OneToOneField(getattr(settings,"AUTH_USER_MODEL","auth.User"),on_delete=models.CASCADE)

    class Mata:
        abstract = True

class UserSession(Session):
    def __str__(self):
        return "< session_id:%s,user_id:%s>" (self.session_id,self.user.id)
