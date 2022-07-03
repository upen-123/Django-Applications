from cattle.models import Cattle, Devices
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from microservice import logger


class GetAllCattleSchema(Schema):
    cattle_id = fields.UUID(required=False)

    @validates("cattle_id")
    def validate_cattle_id(self, value):
        cattle = Cattle.objects.filter(id=value)
        if not cattle:
            logger.error("No entry for cattle id exists in system.")
            raise ValidationError("No entry for cattle id exists in system")
            # check of account active
        if not cattle[0].account.is_active:
            logger.error("User Account is not active in system.")
            raise ValidationError("User Account is not active in system")
        return value


class CattleDeviceMappingSchema(Schema):
    mac_id = fields.Str(required=False)
    start_time = fields.Date(required=False)
    end_time = fields.Date(required=False)
    cattle_id = fields.UUID(required=False)

    @validates("cattle_id")
    def validate_cattle_id(self, value):
        cattle = Cattle.objects.filter(id=value)
        if not cattle:
            logger.error("No entry for cattle id exists in system.")
            raise ValidationError("No entry for cattle id exists in system")
        return value

    @validates("mac_id")
    def validate_mac_id(self, value):
        obj = Devices.objects.filter(mac_id=value)
        if not obj:
            logger.error("Device mac id doesn't exist in system.")
            raise ValidationError("Device mac id doesn't exist in system.")
        return value

    @validates_schema
    def validate_fields(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if (start_time and not end_time) or (end_time and not start_time):
            logger.error("start_time and end_time both should be provided.")
            raise ValidationError("start_time and end_time both should be provided.")
        return data


class CreateCattleActivityAlertSchema(Schema):
    cattle_id = fields.UUID(required=True)
    alert_time = fields.DateTime(
        required=True, format="%Y-%m-%d %H:%M:%S", error_messages={"required": "Alert Warning Time is required."}
    )
    activity_status = fields.Str(required=True)

    @validates("cattle_id")
    def validate_cattle_id(self, value):
        cattle = Cattle.objects.filter(id=value)
        if not cattle:
            logger.error("No entry for cattle id exists in system.")
            raise ValidationError("No entry for cattle id exists in system")
        if not cattle[0].account.is_active:
            logger.error("User Account is not active in system.")
            raise ValidationError("User Account is not active in system")
        return value

    @validates("activity_status")
    def validate_activity_status(self, value):
        valid_activity_status = ["low", "high"]
        if value not in valid_activity_status:
            logger.error("Allowed values for activity_status is high/low")
            raise ValidationError("Allowed values for activity_status is high/low")
        return value
