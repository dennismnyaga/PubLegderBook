from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ClubGetOperations(APIView):
    def post(self, request, format=None):
        print('data here', request.user)
        dat = Club.objects.filter(Owner = request.user)
        
        serialize = ClubSerializer(dat, many = True)
        
        return Response(serialize.data)

class ClubsOperations(APIView):
    # def get(self, request, format=None):
    #     dat = Club.objects.all()
        
    #     serialize = ClubSerializer(dat, many = True)
    #     return Response(serialize.data)
    
    
    def post(self, request, format=None):
        print('data ', request.data)
        print('user ', request.user)
        serializer = AddClubSerializer(data=request.data)
        
        if serializer.is_valid():
            print("This ", serializer.validated_data)
            serializer.save(Owner=request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('This is the error ', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk, format=None):
        try:
            instance = Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            return Response({"error": "Product does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddClubSerializer(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            return Response({"error": "Club does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"Success": "Club deleted!"},status=status.HTTP_204_NO_CONTENT)