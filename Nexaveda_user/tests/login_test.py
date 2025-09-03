

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.cache import cache
import uuid

User = get_user_model()

class AuthTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test@gmail.com", 
            password = "Password@9848"
        )
        self.login_url = reverse('Nexaveda_user:login')
        self.signup_url = reverse('Nexaveda_user:signup')
        self.logout_url = reverse('Nexaveda_user:logout')
        self.forgot_password_rul = reverse('Nexaveda_user:reset_password')
        self.reset_password_url = reverse('Nexaveda_user:reset-password-verify')
        
    def test_user_signup(self):
        response = self.client.post(self.signup_url, {"email": "newtest@gmail.com","password" : "new@984843", "password2": "new@984843", "role":"ADMIN"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,)
    
    def test_user_login(self):
        response = self.client.post(self.login_url,{
            "login" : "test@gmail.com",
            "password" : "Password@9848"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        
    def test_user_logout(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {"refresh" : str(refresh)}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        
    def test_forgot_pasword(self):
        response = self.client.post(self.forgot_password_rul,{"email" : "test@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        
        token = cache.get(f'reset_token:{self.user.email}')
        self.assertIsNotNone(token)
        
    def test_reset_password(self):
        token = str(uuid.uuid4)
        cache.set(f'reset_token:{self.user.email}', token, timeout = 600)
        
        response = self.client.post(self.reset_password_url, {
            "email":"test@gmail.com",
            "token" : token,
            "new_password" : "Newpassword@9848"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Newpassword@9848"))
        
    def test_invalid_reset_token(self):
        cache.set(f'reset_token:{self.user.email}', "validtoken", timeout = 600)
        response = self.client.post(self.reset_password_url, {
            "email" : "test@gmail.com",
            "token" : "wrongtoken",
            "new_password" : "Newpassword@9890"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or Expired token", response.data["message"])