from django.contrib.auth.models import AbstractUser ,Permission
from django.db import models
from django.utils import timezone 


#model for role field       
class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)


    class Meta:
        db_table = "role"

#common model for user and subuser
class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='created_sub_users',null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table="user"
    
    def __str__(self) -> str:
        return self.username


#model for users
class CustomUser(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_user"
        



#model for subuser
class SubuserRole(models.Model):
    name = models.CharField(max_length=50,unique=True)


    class Meta:
        db_table = "subuser_role"

# model for sub user 
class SubUser(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_users')
    subuser_role = models.ForeignKey(SubuserRole,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_subusers_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subuser"




class Bookshop(models.Model):
    book_title = models.CharField(max_length=200,unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'bookshop'
        permissions = [
            ('can_change_bookshop','can change bookshop'),
        ]
    def __str__(self):
        return self.book_title

class Flowershop(models.Model):
    flower_name = models.CharField(max_length=200,unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flowershop'
        permissions = [
            ('can_change_flowershop','can change flowershop'),
        ]
    
    def __str__(self):
        return self.flower_name


class Dish(models.Model):
    dish_name = models.CharField(max_length=200,unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='dishshop'
        permissions = [
            ('can_change_dish','can change dish'),
        ]
    def __str__(self):
        return self.dish_name

class Electronicsshop(models.Model):
    name = models.CharField(max_length=200,unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'electronicsshop'    
        permissions = [
            ('can_change_electronicsshop','can change electronicsshop'),
        ]
       
class UserPermissionAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    assigned_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'permission']

    
