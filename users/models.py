from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    profile_pic = models.ImageField(upload_to = 'user_images', null=True, blank=True, default='https://res.cloudinary.com/djmtfxn8e/image/upload/v1711895043/istockphoto-1495088043-612x612_luc76o.jpg')
    # is_email_verified = models.BooleanField(default=False)
    # is_phone_verified = models.BooleanField(default=False)
    # otp = models.CharField(max_length=10, null=True, blank=True)
    # forgot_password_token = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    


# class VerifiedEmail(models.Model):
#     email = models.EmailField()
#     otp_number = models.CharField(max_length = 200)
#     is_email_verified = models.BooleanField(default = False)
#     timeout = models.DateTimeField(auto_now = True)
    
#     def __str__(self):
#         return self.email



# class VerifiedPhone(models.Model):
#     phone = models.CharField(max_length=20)
#     otp_number = models.CharField(max_length=200)
#     is_phone_verified = models.BooleanField(default=False)
#     timeout = models.DateTimeField(auto_now = True)
    
#     def __str__(self):
#         return self.phone