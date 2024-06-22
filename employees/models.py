from django.db import models
from clubs.models import Club
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class employeesAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idNumber = models.CharField(max_length=200, blank=True, null=True)
    place_of_residence = models.CharField(max_length=200, blank=200, null=200)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    id_front_picture = models.ImageField(upload_to='employees_id', null=True, blank=True)
    id_back_picture = models.ImageField(upload_to='employees_id', null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    # email = models.EmailField(null=True, blank=True)
    
    
    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'