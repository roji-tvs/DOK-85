# User_register/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    # path('register/<int:id>/', UserDetailAPIView.as_view(), name='user-details'),  
    path('login/', UserLoginAPIView.as_view()),
    # path('getuser/', UserDetailAPIView.as_view()),
    path('user_access/', UserProfileAccessAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('create_sub_user/',SubUserCreateAPIView.as_view()),
    # path('subuser_login/',SubuserLoginAPIView.as_view()),
    path('book/',BookAPIView.as_view()),
    path('flower/',FlowerAPIView.as_view()),
    path('dish/',DishAPIView.as_view()),
    path('electronics/',ElectronicsAPIView.as_view()),
    path('model/register/',ModelregisterAPIView.as_view()),
    path('model/access_check/',SubuserModelAccessListAPIView.as_view()),
]   