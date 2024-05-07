from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
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
       
        serializer = AddProductSerializer(data=request.data)
        
        if serializer.is_valid():
            print("This ", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
       
        serializer = AddStockSerializer(data=request.data)
        print('Serializer ', serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

   
class SalesOperations(APIView):
    def get(self, request, format=None):
        dat = SalesRecord.objects.all()
        
        serialize = SalesRecordSerializer(dat, many = True)
        
        return Response(serialize.data)
    
    
    def post(self, request, format=None):       
        serializer = AddSalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        try:
            instance = SalesRecord.objects.get(pk=pk)
        except SalesRecord.DoesNotExist:
            return Response({"error": "Stock does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddSalesSerializer(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():         
            serializer.save()
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
    