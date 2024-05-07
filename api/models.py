from django.db import models
from employees.models import employeesAccount
from clubs.models import Club


class Products(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    buying_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    
    
    def __str__(self):
        return self.name
    
   


class Stocks(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=50, decimal_places=2,null=True, blank=True)
    total_price = models.DecimalField(max_digits=50, decimal_places=2,null=True, blank=True)
    date_stocked = models.DateField(null=True, blank=True)
    who_stocked = models.ForeignKey(employeesAccount, on_delete=models.CASCADE)
    receipt_picture = models.ImageField(upload_to='receipts', null=True, blank = True)
    # edited = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.product_name.name
    
    
class StocksEdited(models.Model):
    who_stocked = models.ForeignKey(employeesAccount, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    edited = models.BooleanField(default=True)
    date_time_edited = models.DateTimeField(auto_now=True)
    
    
class SalesRecord(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    employee = models.ForeignKey(employeesAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.product.product_name.name
    
 
 
class Expenses(models.Model):
    pub = models.ForeignKey(Club, on_delete=models.CASCADE)
    employee = models.ForeignKey(employeesAccount, on_delete=models.CASCADE)
    expense = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField()
    receipt_picture = models.ImageField(upload_to='expenes_reciept', null=True, blank=True)
    
    def __str__(self):
        return self.expense