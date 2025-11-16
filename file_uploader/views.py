from django.shortcuts import render
from django.db import models

# Create your models here.
from django.http import HttpResponse
from file_uploader.forms import UploadFileForm


def fileUploaderView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload(request.FILES['file'])
            return HttpResponse("<h2>File uploaded successful!</h2>")
        else:
            return HttpResponse("<h2>File uploaded not successful!</h2>")

    form = UploadFileForm()
    return render(request, 'D:\\python 2\\Django\\mysite\\file_uploader\\templates\\file_uploader\\upload.html', {'form': form})


def upload(f):
    with open(f.name, 'wb+') as file:
        for chunk in f.chunks():
            file.write(chunk)

