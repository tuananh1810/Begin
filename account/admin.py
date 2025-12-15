from django.contrib import admin

# Register your models here.

from account.models import *
admin.site.register(System)
admin.site.register(Region)
admin.site.register(Account)