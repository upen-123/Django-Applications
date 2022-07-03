from django.urls import path

from account import auth

urlpatterns =[
    path('register-account/',auth.RegisterAccount,name = "account"),
    path("log-in/", auth.login, name="log-in"),
    path("log-out/", auth.logout, name="log-out"),
    path("get-profile/", auth.getUserProfile, name="get-profile"),
    path("update-profile/",auth.UpdateUserInfo, name="update-info"),
]
