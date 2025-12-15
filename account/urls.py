from django.contrib import admin
from django.urls import path
from .views import RegisterAPI , LoginAPI, AccountList


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('account/',AccountList.as_view(), name='list account' )
]