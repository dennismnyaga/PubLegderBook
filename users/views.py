from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['email'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    

@api_view()
def users(request):
    user = User.objects.all()
    serialize = UserSerializer(user, many = True)
    return Response(serialize.data)



@api_view(['POST'])
def user_registration(request):
    serializer = UserRegSerializer(data=request.data)
    print('The register data is ', request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('there is an error ', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)