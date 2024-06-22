from django.contrib import admin
from .models import Club

# Register your models here.


@admin.register(Club)
class clubApi(admin.ModelAdmin):
    list_display = [
        'name'
    ]


# @admin.register(Owner)
# class ownerApi(admin.ModelAdmin):
#     list_display = [
#         'first_name', 'last_name'
#     ]
    
    
