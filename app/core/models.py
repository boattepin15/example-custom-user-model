from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  
    BaseUserManager, 
)
from django.conf import settings


class UserManager(BaseUserManager):
    """ สร้างระบบ จัดการผู้ใช้งานและผู้ดูแล"""
    def create_user(self, email, password=None, **extra_fields):
        """ สร้างระบบสมัครสมาชิกสำหรับผู้ใช้งานทั่วไป"""

        if not email:
            #ตรวจสอบว่ามีการใส่ Email หรือเปล่า
            raise ValueError('โปรดกรอก Email เพื่อสมัครสมาชิก')
        if extra_fields['username'] or 'username' not in extra_fields:
            raise ValueError('โปรดกำหนด Username')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        print(user)
        #เมื่อเชิฟ ผู้ใช้งานใหม่เสร็จ ก็จะส่ง user 
        return user
    

class User(AbstractBaseUser, BaseUserManager):
    """ สร้าง User model Custom จาก AbstractBaseUser"""
    #กำหนด Feild สำหรับ models
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    objects = UserManager()
    USERNAME_FIELD = 'email' #กำหนดให้ใช้ Field email สำหรับ 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username




