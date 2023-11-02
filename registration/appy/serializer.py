from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import HiddenField
from django.contrib.auth.hashers import make_password
from .models import *
from .models import UserPermissionAssignment



# serializer for common model for both user and subuser
class CustomUserSerializer(serializers.ModelSerializer):
    # role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)  
    

    def create(self, validated_data):
        # Hash the password before saving the user object
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)
        user.save()
        return user
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'dob', 'gender', 'mobile_number','first_name','last_name','role','created_by','updated_at']
        extra_kwargs = {'password': {'write_only': True}}   

#serializer for customuser model 
class UserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Nested serializer for User
    
    class Meta:
        model = CustomUser
        fields = "__all__"

# serializer for subuser model 
class SubUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()  # Nested serializer for User
    
    class Meta:
        model = SubUser
        fields = ( 'subuser_role', 'created_by', 'created_at', 'updated_at')



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
class UserPermissionAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionAssignment
        fields = '_all_'