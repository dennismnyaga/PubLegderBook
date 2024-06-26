# Generated by Django 4.2.7 on 2024-06-07 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AdvancesType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Advances_type', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.CharField(blank=True, max_length=500, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateField()),
                ('receipt_picture', models.ImageField(blank=True, null=True, upload_to='expenes_reciept')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('buying_price', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=50)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('date_stocked', models.DateField(blank=True, null=True)),
                ('receipt_picture', models.ImageField(blank=True, null=True, upload_to='receipts')),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StocksEdited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited', models.BooleanField(default=True)),
                ('date_time_edited', models.DateTimeField(auto_now=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stocks')),
            ],
        ),
    ]
