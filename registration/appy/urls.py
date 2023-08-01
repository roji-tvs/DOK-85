# User_register/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('register/<int:id>/', UserDetailAPIView.as_view(), name='user-details'),  
    path('login/', UserLoginAPIView.as_view()),
    path('getuser/', UserDetailAPIView.as_view()),
    path('user_access/<int:id>/', UserProfileAccessAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('create_sub_user/',SubUserCreateAPIView.as_view()),
    path('sub_user_list/<int:id>/',UserSubUserListAPIView.as_view()),
]