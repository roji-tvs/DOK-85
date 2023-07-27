# user_register/urls.py
from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserDetailAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('register/<int:id>/', UserDetailAPIView.as_view(), name='user-details'),  
    path('login/', UserLoginAPIView.as_view()),
    path('getuser/', UserDetailAPIView.as_view()),
    
]



