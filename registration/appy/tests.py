from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .serializer import *
# Create your tests here.

class UserRegistrationAPIViewTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-registration')

    def test_user_registration_valid_data(self):
        # Prepare valid registration data
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'role': 'user',  
            'dob':'01-02-2001',
            'mobile_number':'112233445',
            'gender':'F'
        }
        response = self.client.post(self.register_url, data, format='json')
        breakpoint()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), True)

    def test_user_registration_missing_passwords(self):
        # Write test case to test user registration with missing passwords and other required fields
        data = {
            'username': 'testuser',
            # 'password': 'testpassword',
            # 'password2': 'testpassword',
            'role': 'user',  
            'dob':'01-02-2001',
            'mobile_number':'112233445',
            'gender':'F'
            
            
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), False)
    def test_user_registration_password_not_matching(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword2',
            'password2': 'testpassword1',
            'role': 'user',  
            'dob':'01-02-2001',
            'mobile_number':'112233445',
            'gender':'F'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), False)

    def test_user_registration_superuser_not_allowed(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'role': 'Superuser',  
            'dob':'01-02-2001',
            'mobile_number':'112233445',
            'gender':'F'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), False)

    