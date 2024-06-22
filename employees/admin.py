from django.contrib import admin
from .models import employeesAccount
# Register your models here.


@admin.register(employeesAccount)
class employeesAccountApi(admin.ModelAdmin):
    list_display = [
        # 'first_name',
        # 'last_name',
        'idNumber',
        'place_of_residence',
        'club'
    ]
