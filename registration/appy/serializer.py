from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import HiddenField
from django.contrib.auth.hashers import make_password
from .models import *



# User=get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)  
    # created_by = HiddenField(default=serializers.CurrentUserDefault())
 
     
    def create(self, validated_data):
        # Hash the password before saving the user object
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'dob', 'gender', 'mobile_number','first_name','last_name','role','created_by')
        extra_kwargs = {'password': {'write_only': True}}   

# class SubUserSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         # Hash the password before saving the user object
#         password = validated_data.pop('password')
#         user = SubUser(**validated_data)
#         user.password = make_password(password)
#         user.save()
#         return user
#     class Meta:
#         model = SubUser
#         fields =('username','password','created_by')
#         extra_kwargs = {'password': {'write_only': True}} 


class BookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Bookshop
        fields = '__all__'
class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flowershop 
        fields = '__all__'
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
class ElectronicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Electronicsshop
        fields = '__all__'
class ModellistSerializer(serializers.ModelSerializer):
    class Meta:
        model= ModelList
        fields = '__all__'
class UsermodelpermissionSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField( required=True)
    class Meta:
        model =UserModelPermission
        fields = '__all__'