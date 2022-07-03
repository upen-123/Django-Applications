from django.contrib.auth import get_user_model
from marshmallow import Schema, fields, validate, validates, ValidationError
from django.conf import settings

from number_finder.models import Users

User = get_user_model()


class PhoneNumberDetailsSchema(Schema):
    id = fields.UUID(dump_to="user_id")
    name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)
    is_spam = fields.Boolean(default=False, load_only=True)
    is_user_spam = fields.Method("find_user_spam", dump_only=True)

    def find_user_spam(self, obj):
        if obj.spam_count > settings.SPAM_COUNT_LIMIT:
            return True
        return False

    @validates("phone_number")
    def validate_mobile_number(self, value):
        if len(value) != 10 and not value.isdigit():
            raise ValidationError("Please enter valid phone number."["phone_number"])

        if Users.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number alraedy exist in system.", ["phone_number"])


class UpdateSpamCount(Schema):
    is_spam = fields.Boolean(default=False)
    pass
