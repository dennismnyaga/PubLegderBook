# Generated by Django 4.2.7 on 2024-06-09 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_salesrecord_opening_stock_alter_products_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesrecord',
            name='closing_stock',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
    ]