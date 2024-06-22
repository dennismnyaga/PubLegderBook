from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from django.utils.dateparse import parse_date
from django.db.models import Prefetch
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
        print('Request data ', request.data)
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

    
    
    # def post(self, request, format=None):
    #     selected_date = request.data.get('selectedDate')
    #     selected_club = request.data.get('selectedClub')
    #     dat = SalesRecord.objects.all()
        
        
    #     if selected_date:
    #         parsed_date = parse_date(selected_date)
    #         if parsed_date:
    #             dat = dat.filter(sales_date=parsed_date)
    #             print('Data ', dat)
        
    #     if selected_club:
    #         dat = dat.filter(club__id=selected_club)
            
    #     serialize = SalesRecordSerializer(dat, many = True)
        
    #     return Response(serialize.data)
   
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
    