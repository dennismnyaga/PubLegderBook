from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Club(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name