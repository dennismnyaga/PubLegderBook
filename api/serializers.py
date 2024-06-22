from rest_framework import serializers
from .models import *
from clubs.serializers import *





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        
        
        

        
        
        
class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'buying_price', 'selling_price')
        
    def create(self, validated_data):
        print('validate_data ', validated_data)
        return Products.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        print('Updating')
        # instance.title = validated_data.get('title', instance.title)
        instance.name = validated_data.get('name', instance.name)
        instance.buying_price = validated_data.get('buying_price', instance.buying_price)
        instance.selling_price = validated_data.get('selling_price', instance.selling_price)
        
        instance.save()
        
        return instance






class StockEditSerializer(serializers.ModelSerializer):
    # product_name = ProductSerializer()
    class Meta:
        model = StocksEdited
        fields = '__all__'
        
        

class AddStockEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = StocksEdited
        fields = '__all__'
        
    def create(self, validated_data):
        print('Validated data is ', validated_data)
        return StocksEdited.objects.create(**validated_data)
        
        


class StockSerializer(serializers.ModelSerializer):
    product_name = ProductSerializer()
    class Meta:
        model = Stocks
        fields = '__all__'
        
        
    def create(self, validated_data):
        return Stocks.objects.create(**validated_data)
        
        
        
class AddStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = ('id', 'club', 'product_name', 'quantity', 'date_stocked', 'receipt_picture')
        
    def create(self, validated_data):
        return Stocks.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.club = validated_data.get('club', instance.club)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.date_stocked = validated_data.get('date_stocked', instance.date_stocked)
        instance.who_stocked = validated_data.get('who_stocked', instance.who_stocked)
        instance.receipt_picture = validated_data.get('receipt_picture', instance.receipt_picture)
        
        instance.save()
        
        return instance


# ---------------------Sales record--------------


class SalesRecordSerializer(serializers.ModelSerializer):
    # club = ClubSerializer()
    # product = StockSerializer()
    class Meta:
        model = SalesRecord
        fields = '__all__'
        
        
class StocksSerializer(serializers.ModelSerializer):
    sales_records = SalesRecordSerializer(many=True, read_only=True, source='sales_records_prefetched')
    product_name = ProductSerializer()
    class Meta:
        model = Stocks
        fields = '__all__'       



class AddSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = '__all__'
        
    def create(self, validated_data):
        return SalesRecord.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        instance.club = validated_data.get('club', instance.club)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.product = validated_data.get('product', instance.product)
        
        
        instance.save()
        
        return instance


# ---------------------------expenses--------------------------



class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        
        
        

class AddExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        
    def create(self, validated_data):
        return Expenses.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        print('Here too')
        instance.pub = validated_data.get('pub', instance.pub)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.expense = validated_data.get('expense', instance.expense)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.date = validated_data.get('date', instance.date)
        instance.receipt_picture = validated_data.get('receipt_picture', instance.receipt_picture)
        
        
        instance.save()
        
        return instance

