from django.urls import path 
from . import views

urlpatterns =[
    path('File_Uploader', views.fileUploaderView, name = 'File_uploader')
]