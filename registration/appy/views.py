# user_register/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth import  login  
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .permissions import *
from .serializer import *
from django.contrib.auth.models import Permission
from datetime import datetime




# User=get_user_model()
class UserRegistrationAPIView(APIView):
    def post(self, request):
        password = request.data.get('password')
        password2 = request.data.get('password2')
        role = request.data.get('role')

        if not password or not password2:
            return Response({'msg': 'Please provide both passwords.'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response({'msg': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if role not in [1,2]:
            return Response({'msg': 'Only admin and regular users can register.'}, status=status.HTTP_400_BAD_REQUEST)
    
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
       
    

    def get(self, request):
     id = request.data.get('id')
     if id is not None:
        try:
            usr =User.objects.get(pk=id)
            serializer =CustomUserSerializer(usr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"msg": "user not found"}, status=status.HTTP_404_NOT_FOUND)
     else:
        return Response({'msg': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)


    
    def put(self,request):
        id = request.data.get('id')
        if id is not None:
           try:
              usr = User.objects.get(pk=id)
              serializer = CustomUserSerializer(usr,data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response({'msg':'user updated successfully'},status=status.HTTP_200_OK)
              return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
           except User.DoesNotExist:
            return Response({"msg": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'msg': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)


    
    def delete(self, request):
        id=request.data.get('id')
        try:
           usr = User.objects.get(pk=id)
        except User.DoesNotExist:
           return Response({"msg": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        usr.delete()
        return Response({'msg': 'user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
# class UserDetailAPIView(APIView):
#    def get(self, request):
#         users = User.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return Response(serializer.data)
   
        

class UserLoginAPIView(APIView):
    
    def post(self, request):
        mobile_number= request.data.get('mobile_number')
        password = request.data.get('password')
        try:
           
           user=User.objects.get(mobile_number=mobile_number)  
        except:
            return Response({"message": "User with the provided phone number not found."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if check_password(password, user.password): #Check if the provided password matches the stored password hash
            # 'login' method logs in the user for the current request
            login(request, user)
            refresh = RefreshToken.for_user(user)

            return Response({"message": "Login successful.", 'refresh': str(refresh),
                            'access': str(refresh.access_token),}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid password credentials."}, status=status.HTTP_401_UNAUTHORIZED)


#api for get user info based on role       
class UserProfileAccessAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({'msg': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        role = user.role    
        if role == "Superuser":  # Superuser (1)
            # Superuser can access all user profiles
            users1 = User.objects.all()
            # usr = SubUser.objects.all()
            serializer = CustomUserSerializer(users1, many=True)
            # serializer2 = SubUserSerializer(usr, many=True)
            data1 = {
                'all_profiles' : serializer.data,
                # 'all_subuser_profile' : serializer2.data,
            }
            return Response(data1, status=status.HTTP_200_OK)
        elif role == "Admin":
            # admin can only access his profile and all users profile
            admin = request.user
            users2 = User.objects.filter(role="user")  # User (3) profiles only
            serializer_admin = CustomUserSerializer(admin)
            serializer_users = CustomUserSerializer(users2, many=True)
            data2 = {
                'admin_profile': serializer_admin.data,
                'user_profiles': serializer_users.data,
            }
            return Response(data2, status=status.HTTP_200_OK)
        elif role == "user": # Regular User (3)
            # Regular user can only access their own profile and created subuser by them
            serializer = CustomUserSerializer(user)
            sub_users = user.created_sub_users.all()
            serializer2 =CustomUserSerializer(sub_users,many=True)
            # serializer2 = SubUserSerializer(sub_users, many=True)
            # if not serializer2.data:  # If the serialized data is empty
            #     return Response({'message': 'No sub_user created by this user'}, status=status.HTTP_200_OK)
            data3 = {
                'user_profile': serializer.data,
                'created_sub_users': serializer2.data
            }
            return Response(data3, status=status.HTTP_200_OK)
        else:
            # Invalid or unsupported role
            return Response({'msg': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)
        
# Login Api for subuser login         
# class SubuserLoginAPIView(APIView):
#     def post(self,request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         # try:
#         #     user = SubUser.objects.get(username=username)
#         # except SubUser.DoesNotExist:
#         #     return Response({'msg':'subuser with provided username does not exist'},status=status.HTTP_404_NOT_FOUND)
#         if check_password(password, user.password):
#             # refresh = RefreshToken.for_user(user)

#             return Response({"message": "Login successful.", }, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Invalid password credentials."}, status=status.HTTP_401_UNAUTHORIZED)
       
               
#api for creating sub-user     
class SubUserCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.user.id
        

        data = request.data.copy()
        
        data['created_by'] = user_id
        data['role']= 3
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Sub-user created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# api for bookshop

class BookAPIView(APIView):
    permission_classes = [IsAuthenticated,CanChangeBookshopPermission]
    authentication_classes = [JWTAuthentication]
   
    
        
    def get(self, request):
        
        
        books = Bookshop.objects.all()
        serializer=BookSerializer(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        
        id = request.data.get('id')
        try:
            books = Bookshop.objects.get(pk=id)
        except Bookshop.DoesNotExist:
            return Response({"msg": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(books, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Book updated successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#api for flowershop    

class FlowerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,CanChangeFlowershopPermission]
    
    
    def get(self, request):
        
        flos = Flowershop.objects.all()
        serializer=FlowerSerializer(flos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        user_id = request.user.id
        
        serializer = FlowerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        id = request.data.get('id')
        
        try:
            flos= Flowershop.objects.get(pk=id)
        except Flowershop.DoesNotExist:
            return Response({"msg": "flower not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FlowerSerializer(flos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'flower updated successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# api for dishshop 

class DishAPIView(APIView):
    permission_classes = [IsAuthenticated,CanChangeDishPermission]
    authentication_classes = [JWTAuthentication]
           
    # Check if the user has access to the specified model_id in UserModelPermission
    
    def get(self, request):
        
        dish = Dish.objects.all()
        serializer=DishSerializer(dish, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = DishSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        id = request.data.get('id')
        
        
        try:
            dish= Dish.objects.get(pk=id)
        except Dish.DoesNotExist:
            return Response({"msg": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DishSerializer(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Dish updated successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# api for electronicshop

class ElectronicsAPIView(APIView):
    permission_classes = [IsAuthenticated,CanChangeElectronicsshopPermission]
    authentication_classes = [JWTAuthentication]

        
    def get(self, request):
        
        electro = Electronicsshop.objects.all()
        serializer=ElectronicsSerializer(electro,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer= ElectronicsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        id = request.data.get('id')
        
        
        try:
            electro= Electronicsshop.objects.get(pk=id)
        except Electronicsshop.DoesNotExist:
            return Response({"msg": "this Electronic gadget not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ElectronicsSerializer(electro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'updated successfully'}, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def delete(self, request):
    #     id = request.data.get('id')
    #     try:
    #         book = Electronicsshop.objects.get(pk=id)
    #     except Electronicsshop.DoesNotExist:
    #         return Response({"msg": "Gadget not found"}, status=status.HTTP_404_NOT_FOUND)

    #     book.delete()
    #     return Response({'msg': 'Gadget deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#register model in model_list


class AssignPermission(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrRegularUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.user.id
        # user_role = request.user.role  # Assuming 'role' is the attribute representing user roles
        
        
        # request_user=User.objects.get(id=requesting_user_id)
        # print(request_user.role)
        # if request_user.role != 1 and request_user.role != 2:
        #     return Response({"You do not have permission to assign  permissions to subusers."},
        #                     status=status.HTTP_403_FORBIDDEN)
        

        username = request.data.get('username')
        model_names = request.data.get('model_names')  # Change to 'model_names' to receive a list

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User with the provided username does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        permissions_assigned = []
        permissions_already_assigned = {}

        for model_name in model_names:
            

            permission_codename = f'can_change_{model_name}'
            try:
                permission = Permission.objects.get(codename=permission_codename)
            except Permission.DoesNotExist:
                return Response({"message": f"Permission '{permission_codename}' does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            # Check if the permission is already assigned to the user for this model
            existing_assignment = UserPermissionAssignment.objects.filter(user=user, permission=permission).first()
            if existing_assignment:
                permissions_already_assigned[model_name] = existing_assignment.assigned_datetime.isoformat()
            else:
                # Assign the permission to the user
                UserPermissionAssignment.objects.create(user=user, permission=permission)
                permissions_assigned.append(model_name)

        # Record the assignment details
        assignment_details = {
            "username": user.username,
            "permissions_assigned": permissions_assigned,
            "permissions_already_assigned": permissions_already_assigned,
            "permission_given_by": user_id 
        }

        return Response({"message": "Permissions assigned successfully.", "assignment_details": assignment_details},
                        status=status.HTTP_200_OK)



class RemovePermission(APIView):
    permission_classes = [IsAuthenticated,  IsAdminOrRegularUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        requesting_user_id = request.user.id
        # # user_role = request.user.role  # Assuming 'role' is the attribute representing user roles
        # request_user=User.objects.get(id=requesting_user_id)
        # # print(request_user.role)
        # if request_user.role != 1 and request_user.role != 2:
        #     return Response({"You do not have permission to remove permissions to subusers."},
        #                     status=status.HTTP_403_FORBIDDEN)
        
        username = request.data.get('username')
        model_names = request.data.get('model_names')  # Change to 'model_names' to receive a list

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User with the provided username does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        permissions_removed = []
        permissions_not_assigned = {}

        for model_name in model_names:
            
            permission_codename = f'can_change_{model_name}'
            try:
                permission = Permission.objects.get(codename=permission_codename)
            except Permission.DoesNotExist:
                return Response({"message": f"Permission '{permission_codename}' does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

            # Check if the permission is assigned to the user for this model
            existing_assignment = UserPermissionAssignment.objects.filter(user=user, permission=permission).first()
            if existing_assignment:
                # Record the timestamp before removing the permission
                removed_datetime = existing_assignment.assigned_datetime
                existing_assignment.delete()
                permissions_removed.append((model_name, removed_datetime))
            else:
                permissions_not_assigned[model_name] = "Permission not assigned"

        # Record the removal details
        removal_details = {
            "username": user.username,
            "permissions_removed": permissions_removed,
            "permissions_not_assigned": permissions_not_assigned,
            "permission_removed_by": requesting_user_id
        }

        return Response({"message": "Permissions removed successfully.", "removal_details": removal_details},
                        status=status.HTTP_200_OK)      

# class SubUserProfileListAPIView(APIView):
#     def get(self,request): 



