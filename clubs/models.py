from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Owner(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.first_name

class Club(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    Owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name