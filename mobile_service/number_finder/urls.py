from django.urls import path

from number_finder.api.phone_number import CreateUserDetail, GetPhoneNumberDetail, UpdatePhoneNumberDetail

urlpatterns = [
    path("create-user/", CreateUserDetail.as_view(), name="create_user"),
    path("get-user/", GetPhoneNumberDetail.as_view(), name="get_user"),
    path("update-user/<uuid:id>/", UpdatePhoneNumberDetail.as_view(), name="get_user"),
    ]