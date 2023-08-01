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
from .models import User
from .serializer import CustomUserSerializer  

# User=get_user_model()
class UserRegistrationAPIView(APIView):
    def post(self, request):
        password = request.data.get('password')
        password2 = request.data.get('password2')
        
        if not password or not password2:
           return Response({'msg':'please provide both  password'})


        if password != password2:
            return Response({'msg': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
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
                return Response({'msg':'user updated successfully'},status=status.HTTP_205_RESET_CONTENT)
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
    
class UserDetailAPIView(APIView):
   def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
   
        

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

    def get(self, request,id):
        
        
        try:
            user = User.objects.get(pk=id)
            role = user.role
            
            if role == "Superuser":  # Superuser (1)
                # Superuser can access all user profiles
                users = User.objects.all()
                serializer = CustomUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif role == "Admin":  # Admin (2)
                # Admin can access their own profile and user profiles
                users = User.objects.filter(role__in=['Admin','user'])  # Admin (2) and User (3)
                serializer = CustomUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif role == "user": # Regular User (3)
                # Regular user can only access their own profile
                user = request.user
                serializer = CustomUserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Invalid or unsupported role
                return Response({'msg': 'Invalid role. Supported roles are 1, 2, and 3.'}, status=status.HTTP_400_BAD_REQUEST)
                
        except User.DoesNotExist:
            return Response({'msg': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
#api for creating sub-user     
class SubUserCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.data.get('id')

        if not user_id:
            return Response({'msg': 'Provide a valid id'}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'msg': 'User with the provided id does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        # Set the 'created_by' field to the user'id
        data['created_by'] = user.id
        
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Sub-user created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

class UserSubUserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'msg': 'User with the provided id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        sub_users = user.created_sub_users.all()
        serializer = CustomUserSerializer(sub_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



