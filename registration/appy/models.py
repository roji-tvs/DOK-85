from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('superuser','Superuser'),
        ('admin','Admin'),
        ('user','user'),
        ('sub_user','sub_user')
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES, default='user')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,  related_name='created_sub_users')



    class Meta:
        db_table="user"




