from django.contrib import admin
from django.urls import path
from .views import RegisterAPI , LoginAPI, AccountList , StaffView, StaffDetail, UpdateStatusStaff


urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('account/',AccountList.as_view(), name='list account' ),
    path('staff/', StaffView.as_view(), name='list staff'),
    path('api/v1/staff/<int:pk>', StaffDetail.as_view(), name='staff detail'),
    path('api/v1/update-status-staff/<int:pk>', UpdateStatusStaff.as_view(), name='staff disable'),
]