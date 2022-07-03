from marshmallow import Schema, fields, ValidationError, validates_schema, validates, post_load

from restaurant.models import Cuzzin


class CuzzinBaseSchema(Schema):
    categories = fields.Str(required = False)
    favorites = fields.Str(required = False)
    dishes = fields.Str(required = False)

    @validates('dishes')
    def validate_length(self, value):
        if len(value) < 1:
            raise ValidationError('Quantity must be greater than 0.')


class CreateCuzzinSchema(CuzzinBaseSchema)  :
    user_id = fields.UUID(required=False)
    categories = fields.Str(required=True)
    favorites = fields.Str(required=True)
    dishes = fields.Str(required=True)

class GetCuzzinSchema(Schema):
    cuzzin_id = fields.UUID(required=True)

    @post_load
    def extract_user(self,data):
        cuzzin_id = data["cuzzin_id"]
        try:
            cuzzin = Cuzzin.objects.get(id=cuzzin_id)
        except Cuzzin.DoesNotExist:
            raise ValidationError("cuzzin doesnot exist in the systm")
        data["cuzzin"]=cuzzin
        return data

class UpdateDeleteSchema(CuzzinBaseSchema):
    cuzzin_id = fields.UUID(required=True)
    @validates_schema()
    def validate_fields(self,data):
        categories = data.get("categories")
        favorites = data.get("favorites")
        dishes = data.get("dishes")
        cuzzin_id = data.get("cuzzin_id")

        cuzzin = Cuzzin.objects.filter(id=cuzzin_id)
        if not cuzzin:
            raise ValidationError("Cuzzin doesn't exist in the system")
        data["cuzzin"]=cuzzin[0]
        return data