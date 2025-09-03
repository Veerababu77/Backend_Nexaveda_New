

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()

class AuthTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@gmail.com", 
            password = "Password@9848"
        )
        self.login_url = reverse('login/'),
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        
    def test_user_signup(self):
        response = self.client.post(self.signup_url, {"email": "newtest@gmail.com","password" : "new@984843", "password2": "new@984843"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,)