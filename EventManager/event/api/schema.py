from marshmallow import Schema, fields, post_load, validates_schema, ValidationError

from EventManager.event.models import EventInfo, Users


class UserSchema(Schema):
    first_name = fields.Str(required=True, load_only=True)
    last_name = fields.Str(required=True, load_only=True)
    username = fields.Str(required=True)
    mobile_number = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class EventSchema(Schema):
    name = fields.Str(required=True, dump_to="event_name")
    date = fields.Date(required=True)
    city = fields.Str(required=True)


class EventRatingSchema(Schema):
    model = EventInfo
    user_id = fields.UUID(required=True)
    event_id = fields.UUID(required=True)
    rating = fields.Float(required=True)

    @validates_schema
    def validate_user_id(self, data):
        user_id, event_id = data.get("user_id"), data.get("event_id")
        user = Users.objects.filter(id=user_id).first()
        event = EventInfo.objects.filter(id=event_id).first()

        if not user:
            raise ValidationError("Please provide valid user_id.", ["user_id"])

        if not event:
            raise ValidationError("Event not exist in system.", ["event_id"])

        if not (user.city == event.city):
            raise ValidationError("User and Event should belong from the same city.", ["event_id"])






class UserEventSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    event_id = fields.UUID(required=True)
