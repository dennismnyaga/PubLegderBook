from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import *

   
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'



class UserRegSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    
# class OtpSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = VerifiedEmail
#         fields = "__all__"
        
        
# class OtpUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['otp_number'] 