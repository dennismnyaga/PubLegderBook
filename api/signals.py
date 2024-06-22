from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


   
@receiver(post_save, sender=Stocks)
def create_sales_record(sender, instance, created, **kwargs):
    print('Signal instance ', instance)
    if created:
        SalesRecord.objects.create(
            club=instance.club,
            product=instance,
            opening_stock=instance.quantity,
            sales_date = instance.date_stocked
            # Other fields are left as null or blank
        )