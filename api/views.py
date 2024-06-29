from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from django.utils.dateparse import parse_date
from django.db.models import Prefetch
from django.db.models.signals import post_save
from .signals import create_sales_record
from rest_framework.parsers import JSONParser
# Create your views here.


class StockUpdatedHandles(APIView):
    def get(self, request, format=None):
        dat = StocksEdited.objects.all()
        
        serializer = StockEditSerializer(dat, many = True)
        
        return Response(serializer.data)
        
# -------------------product------------------------

class ProductsOperations(APIView):
    def get(self, request, format=None):
        dat = Products.objects.all()
        
        serialize = ProductSerializer(dat, many = True)
        
        return Response(serialize.data)
    
    
    def post(self, request, format=None):
        print('data ', request.data)
        print('user ', request.user)
        serializer = AddProductSerializer(data=request.data)
        
        if serializer.is_valid():
            print("This ", serializer.validated_data)
            serializer.save(Owner=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('This is the error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        try:
            instance = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response({"error": "Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddProductSerializer(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response({"error": "Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"Success": "Product deleted!"},status=status.HTTP_204_NO_CONTENT)
    
# ---------stocks operation-----------  
    
class StockOperations(APIView):
    def get(self, request, format=None):
        print('called here!')
        dat = Stocks.objects.all()
        
        serialize = StockSerializer(dat, many = True)
        
        return Response(serialize.data)
    
    
    def post(self, request, format=None):
        print('data ', request.data)
        serializer = AddStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(who_stocked = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('Error message ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        print('Updating', request.data['who_stocked'])
        try:
            instance = Stocks.objects.get(pk=pk)
            # print('instance data',request.data)
        except Stocks.DoesNotExist:
            print('Does not exist')
            return Response({"error": "Stock does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        # request.data['edited'] = True
        serializer = AddStockSerializer(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            # print('serial ', serializer.data)
            edited = {
                "who_stocked": int(request.data['who_stocked']),
                "stock" : instance.id,
                "edited": True
            }
            editer = AddStockEditSerializer(data=edited)
            if editer.is_valid():
                editer.save()
            else:
                print('Its not valid!')
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Stocks.objects.get(pk=pk)
        except Stocks.DoesNotExist:
            return Response({"error": "Stock does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"Success": "Stock deleted!"},status=status.HTTP_204_NO_CONTENT)
    
    
    
# -------------------sales records----------------

class SalesGetOperations(APIView):
    def post(self, request, format=None):
        selected_date = request.data.get('selectedDate')
        selected_club = request.data.get('selectedClub')

        # Initial queryset for stocks
        stocks_queryset = Stocks.objects.filter(club__id=selected_club)

        # Optional filtering by date if provided
        if selected_date:
            sales_queryset = SalesRecord.objects.filter(sales_date=selected_date)
        else:
            sales_queryset = SalesRecord.objects.all()

        # Prefetch sales records with the optional date filter
        stocks_queryset = stocks_queryset.prefetch_related(
            Prefetch('salesrecord_set', queryset=sales_queryset, to_attr='sales_records_prefetched')
        )

        print('Stocks queryset:', stocks_queryset)

        # Serialize the queryset
        serialize = StocksSerializer(stocks_queryset, many=True)
        print('Serialized data:', serialize.data)
        return Response(serialize.data)
    
    def put(self, request, format=None):
        print('Data ', request.data)
        stock_id = request.data.get('id')
        stock = get_object_or_404(Stocks, id=stock_id)
       
        
        if 'quantity' in request.data:
            new_quantity = int(request.data.get('quantity'))
            if stock.quantity is None:
                stock.quantity = new_quantity
            else:
                print('stock not present ', stock.quantity)
                stock.quantity += int(new_quantity)
                x = stock.quantity + int(new_quantity)
                print('new data ', x)
            post_save.disconnect(create_sales_record, sender=Stocks)
            stock.save()

            # Update recieved_stock in SalesRecord
            sales_records = SalesRecord.objects.filter(product=stock)
            for sales_record in sales_records:
                if sales_record.recieved_stock is None:
                    sales_record.recieved_stock = int(new_quantity)
                else:
                    sales_record.recieved_stock += int(new_quantity)
                sales_record.save()
                post_save.connect(create_sales_record, sender=Stocks)

 
        stock = Stocks.objects.prefetch_related(
                    Prefetch('salesrecord_set', queryset=sales_records, to_attr='sales_records_prefetched')
                ).get(id=stock_id)
        
        data = request.data
        del data['quantity']
        serializer = StocksSerializer(stock, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            print('Updated data ', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print('This is error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SalesPostSoldOperations(APIView):
    def put(self, request, format = None):
        print('closing stock data ', request.data)
        stock_id = request.data.get('id')
        stock = get_object_or_404(Stocks, id=stock_id)
        
        
        if 'closingStock' in request.data:
            closing_stock = request.data.get('closingStock')
            if stock.quantity is None:
                return Response({'error': 'Stock quantity is not available.'}, status=status.HTTP_400_BAD_REQUEST)
                # stock.quantity = new_quantity
            else:
                print('stock not present ', stock.quantity)
                stock.quantity -= int(closing_stock)
            post_save.disconnect(create_sales_record, sender=Stocks)
            stock.save()

            # Update recieved_stock in SalesRecord
            sales_records = SalesRecord.objects.filter(product=stock)
            for sales_record in sales_records:
                print('sales ', sales_record)
                # if sales_record.closing_stock is None:
                #     sales_record.closing_stock = closing_stock
                # else:
                #     sales_record.recieved_stock = int(closing_stock)
                sales_record.closing_stock = int(closing_stock)
                sales_record.save()
                post_save.connect(create_sales_record, sender=Stocks)

        
        stock = Stocks.objects.prefetch_related(
                    Prefetch('salesrecord_set', queryset=sales_records, to_attr='sales_records_prefetched')
                ).get(id=stock_id)
        
        data = request.data
        del data['closingStock']
        serializer = StocksSerializer(stock, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print('This is error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
class SalesOperations(APIView):
    def get(self, request, format=None):
        dat = SalesRecord.objects.all()
        
        serialize = SalesRecordSerializer(dat, many = True)
        
        return Response(serialize.data)
    
    
    def post(self, request, format=None):       
        serializer = AddSalesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(who_stocked=request.user)
            if sales_record.recieved_stock:
                sales_record.product.quantity += sales_record.recieved_stock
                sales_record.product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        try:
            instance = SalesRecord.objects.get(pk=pk)
        except SalesRecord.DoesNotExist:
            return Response({"error": "Stock does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        initial_received_stock = instance.recieved_stock or 0
        serializer = AddSalesSerializer(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():         
            serializer.save()
            if sales_record.recieved_stock != initial_received_stock:
                stock_difference = (sales_record.recieved_stock or 0) - initial_received_stock
                sales_record.product.quantity += stock_difference
                sales_record.product.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = SalesRecord.objects.get(pk=pk)
        except SalesRecord.DoesNotExist:
            return Response({"error": "Sales does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"Success": "Sales deleted!"},status=status.HTTP_204_NO_CONTENT)
    
    
    
    
# received Stock Operations
class RecieveStockOperations(APIView):
    def Put(self, request, format=None):
        try:
            sales_record = SalesRecord.objects.get(pk=pk)
        except Stocks.DoesNotExist:
            return Response({"error": "Sales Record does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecieveSalesStockOperationsSerializer(instance=instance, data=request.data, partial=True)
        print('Serializer ', serializer)
        if serializer.is_valid():  
            recieved_stock = serializer.validated_data.get('recieved_stock')
            if recieved_stock is not None:
                # Update the Stocks quantity
                stock = sales_record.product
                stock.quantity = stock.quantity + recieved_stock if stock.quantity else recieved_stock
                stock.save()       
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
# -----------------expenses---------------------


class ExpensesOperations(APIView):
    def get(self, request, format=None):
        dat = Expenses.objects.all()
        
        serialize = ExpensesSerializer(dat, many = True)
        
        return Response(serialize.data)
    
    
    def post(self, request, format=None):       
        serializer = AddExpensesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        print("Running!")
        try:
            instance = Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            return Response({"error": "Expense does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddExpensesSerializer(instance=instance, data=request.data, partial=True)
        print('Serializer ', serializer)
        if serializer.is_valid():         
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            return Response({"error": "Expense does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"Success": "Expense deleted!"},status=status.HTTP_204_NO_CONTENT)
    