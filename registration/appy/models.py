from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Superuser','Superuser'),
        ('Admin','Admin'),
        ('user','user'),
        ('subuser','subuser')
       
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,default='Superuser')
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='created_sub_users',null=True)

    class Meta:
        db_table="user"

#model for sub user 
# class SubUser(models.Model):
#     username = models.CharField(max_length=200,unique=True)
#     password = models.CharField(max_length=250)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sub_users')

#     class Meta:
#         db_table = "subuser"




class Bookshop(models.Model):
    book_title = models.CharField(max_length=200,unique=True)

    class Meta:
        db_table = 'bookshop'

class Flowershop(models.Model):
    flower_name = models.CharField(max_length=200,unique=True)

    class Meta:
        db_table = 'flowershop'

class Dish(models.Model):
    dish_name = models.CharField(max_length=200,unique=True)

    class Meta:
        db_table='dishshop'

class Electronicsshop(models.Model):
    name = models.CharField(max_length=200,unique=True)
    class Meta:
        db_table = 'electronicsshop'           

class ModelList(models.Model):
    
    model_id = models.PositiveIntegerField( primary_key=True)
    model_name = models.CharField(max_length=100,unique=True)

    class Meta:
        db_table = 'model_list'

class UserModelPermission(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(ModelList, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "user_model_permission"
        unique_together = ('user', 'model')                   