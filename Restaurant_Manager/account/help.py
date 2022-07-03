from datetime import datetime

from django.contrib.auth import authenticate
from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    """Abstract BaseModel class"""

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)

    created_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.id)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    @classmethod
    def bulk_create(cls, data):
        if isinstance(data, list):
            cls.objects.bulk_create([cls(**row) for row in data])
        else:
            raise ValueError("Not a valid data for bulk operation")

    @classmethod
    def validate_id(cls, id):
        obj = cls.objects.filter(id=id)
        if not obj:
            return False
        return True

    def update_fields(self, obj, **kwargs):
        "Update fields of given users object"
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()

