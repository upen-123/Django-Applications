from django.urls import path

from restaurant import cuzine, ListCuzzin
from restaurant.cuzine import CreateCuisine

urlpatterns = [
#    path("create-cuzzin/",cuzine.CreateCuzzine,name = "cuzzin"),
    path("create-cuzzin/",CreateCuisine.as_view(),name = "cuzzin"),
    path("get-cuzzin/",cuzine.GetCuzzin, name = "get-cuzzin"),
    path("update-cuzzin/",cuzine.UpdateCuzzin, name = "update-cuzzin"),
    path("delete-cuzzin/",cuzine.DeleteCuzzin,name= "delete-cuzzin"),
    path("get-list-cuzzin/",ListCuzzin.ListCuzzins,name="get-cuzzin"),
]