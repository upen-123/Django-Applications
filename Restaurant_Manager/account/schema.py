from marshmallow import Schema, validates_schema, validate, fields, validates, ValidationError, post_load

from account.models import Users


class UserBaseSchema(Schema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    username = fields.Str(required=False)

    @validates("first_name")
    def validate_first_name(self,value):
        return value.strip()
    @validates("last_name")
    def validate_last_name(self,value):
        return value.strip()

    @validates("phone_number")
    def validate_phone_number(self,value):
        value = value.strip()
        if len(value) != 10 :
            raise ValidationError("Incorrect length of phone_number")

class RegisterAccountSchema(UserBaseSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("username")
    def validate_username(self,value):
        value = value.strip()
        if len(value) < 4 :
            raise ValidationError("username  must be contain at least four characters")
        return value

    @validates("password")
    def validate_password(self,value):
        value = value.strip()
        if len(value) < 4 :
            raise ValidationError("password length  must be contain at least four characters")
        return value

class GetUserProfileSchema(UserBaseSchema):
    user_id = fields.UUID(required=True)

    @post_load
    def extract_user(self,data):
        user_id = data["user_id"]
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise ValidationError("user is not there in the system")
        data["user"]=user
        return data

class UpdateAccountSchema(UserBaseSchema):
    user_id = fields.UUID(required=True)

    @validates_schema
    def validate_fields(self,data):
        user_id = data.get("user_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")

        user = Users.objects.filter(id=user_id)
        if not user:
            raise ValidationError("user doesn't exist in the system")
        data["user"]=user[0]
        user = Users.objects.filter(username=username).exclude(id = user_id)
        if user:
            raise ValidationError("username of this name is already exists")
        return data


class LogInSchema(Schema):
    username = fields.Str(required=True, error_messages={"reuired": "username is required parameter"})
    password = fields.Str(required=True, error_messages={"required": "password is required parameter"})