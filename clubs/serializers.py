from rest_framework import serializers
from .models import *





class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'
        
        
        

        
        
        
class AddClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'location')
        
    def create(self, validated_data):
        print('validate_data ', validated_data)
        return Club.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        print('Updating')
        # instance.title = validated_data.get('title', instance.title)
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.buying_price)
        
        instance.save()
        
        return instance



