from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Products)
class productsApi(admin.ModelAdmin):
    list_display = [
        'name', 'buying_price', 'selling_price'
    ]


@admin.register(Stocks)
class stockApi(admin.ModelAdmin):
    list_display = [
        'club', 'product_name', 'quantity', 'total_price', 'date_stocked', 'who_stocked', 'date_edited'
    ]


@admin.register(StocksEdited)
class stocksEditedApi(admin.ModelAdmin):
    list_display = [
        'stock', 'edited', 'date_time_edited'
    ]


@admin.register(SalesRecord)
class salesRecordApi(admin.ModelAdmin):
    list_display = [
        'product', 'quantity', 'date'
    ]


@admin.register(Expenses)
class expensesApi(admin.ModelAdmin):
    list_display = [
        'expense', 'amount', 'date'
    ]
    
    
    
    
@admin.register(AdvancesType)
class AdvancesTypeApi(admin.ModelAdmin):
    list_display = [
        'Advances_type'
    ]
    
    
    
    
@admin.register(Advances)
class AdvancesApi(admin.ModelAdmin):
    list_display = [
        'advances', 'amount', 'date'
    ]