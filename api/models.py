from django.db import models
from employees.models import employeesAccount
from clubs.models import Club
from django.contrib.auth import get_user_model
User = get_user_model()


class Products(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    buying_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    
    
    def __str__(self):
        return self.name
    
   


class Stocks(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=50, decimal_places=2,null=True, blank=True)
    date_stocked = models.DateField(null=True, blank=True)
    who_stocked = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_picture = models.ImageField(upload_to='receipts', null=True, blank = True)
    date_edited = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.product_name.name
    

    
class SalesRecord(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    who_recorded = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    opening_stock = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    closing_stock = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    sales_quantity = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    recieved_stock = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    sales_date = models.DateField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    done = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.product.product_name.name
    
   
    
class StocksEdited(models.Model):
    who_stocked = models.ForeignKey(employeesAccount, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    edited = models.BooleanField(default=True)
    date_time_edited = models.DateTimeField(auto_now=True)
 
class Expenses(models.Model):
    pub = models.ForeignKey(Club, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField()
    receipt_picture = models.ImageField(upload_to='expenes_reciept', null=True, blank=True)
    
    def __str__(self):
        return self.expense


class AdvancesType(models.Model):
    Advances_type = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.Advances_type    
    
class Advances(models.Model):
    advances = models.ForeignKey(AdvancesType, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=50)
    date = models.DateField()
    
    def __str__(self):
        return self.advances.Advances_type
    
    

# advances
# mpesa transactions