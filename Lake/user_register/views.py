# user_register/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login  #logout
#from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer 


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.data['email'])
            if user.exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            user = User(
                    username=request.data['username'],
                     email=request.data['email'],
                   password=make_password(request.data['password'])  # Hash the password
                )
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
     id = request.data.get('id')
     if id is not None:
        try:
            usr = User.objects.get(pk=id)
            serializer = UserSerializer(usr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"msg": "user not found"}, status=status.HTTP_404_NOT_FOUND)
     else:
        return Response({'error': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)


    
    def put(self,request):
        id = request.data.get('id')
        if id is not None:
           try:
              usr = User.objects.get(pk=id)
              serializer = UserSerializer(usr,data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response({'msg':'user updated successfully'},status=status.HTTP_205_RESET_CONTENT)
              return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
           except User.DoesNotExist:
            return Response({"msg": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User ID not provided in the request data'}, status=status.HTTP_400_BAD_REQUEST)


    
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
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
   
        
class UserLoginAPIView(APIView):
    
    def post(self, request):
        #breakpoint()
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)  # Logs in the user for the current request
            return Response({"message": "Login successful.", "user_id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
#class UserLogoutAPIView(APIView):
    #permission_classes = [IsAuthenticated]  

    #def post(self, request):
        #logout(request)  # Logs out the user for the current request
        #return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
       
        

    


