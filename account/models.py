from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)
        

    def get_by_natural_key(self, username):
        return self.get(username=username)
    
class System(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Region(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Account(AbstractUser):
    address = models.TextField(blank=True, null=True, default=None)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, blank= True, null= True )
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank= True, null= True )
    code =  models.CharField(max_length=50, blank= True, null= True, default=None)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, blank= True, null= True,default=None)
    phone = models.CharField(max_length=50, blank= True, null= True,default=None)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_created = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="create_user",default=None)
    objects = UserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



# tạo 1 bảng tên là system trong bảng system lưu title và code để phân chia ng dùng thành 2 system 1 là nhân viên(staff) 2 là admin
# account gắn foreing key là system. mỗi ng có duy nhất 1 role 
# thêm 1 trường address, phone, region(foreing key trong bảng có tiltle và code)