from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import User


# User=get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)   
     
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

    