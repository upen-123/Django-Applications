from django.db import models

# Create your models here.
from account.help import BaseModel
from account.models import Users


class Cuzzin(BaseModel):
    CuzzinID = models.ForeignKey(Users,on_delete=models.CASCADE)
    categories = models.CharField(max_length = 50, blank =True)
    favorites = models.CharField(max_length = 50, blank = True)
    dishes = models.CharField(max_length = 50 , blank = True)


    def __str__(self):
        return "Cuzzin_id: %s" % self.id

    def delete_obj(self, obj):
        obj.delete()
