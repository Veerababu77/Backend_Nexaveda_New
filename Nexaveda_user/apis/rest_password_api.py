
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from validators import validate_phone_number
import random
from utils.helper import send_sms
from django.contrib.auth.hashers import make_password

User = get_user_model()

class ResetPasswordAPI(APIView):
    """
    ResetPasswordAPI is used to reset the current password of a User through Email and Phone Number.

    Args:
        "email":"User email",
        "phone_number" : "Phone number"
    """
    
    def post(self, request):
        
        phone_number = request.data.get('phone_number', None)
        email = request.data.get('email', None)
        
        if not phone_number and not email:
            return Response({"message":"Reset password need email or phone number to proceed"}, status = status.HTTP_400_BAD_REQUEST)
        
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return Response({"message":"Please provide a valid email"}, status = status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email = email).exists():
                token = str(uuid.uuid4())
                cache.set(f"reset_token:{email}", token, timeout = 600)
                send_mail (
                    subject = "Password Reset link.",
                    message = f"Please reset your password by clicking the link below. {token}",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [email],
                    fail_silently = False
                )
                return Response({"message":"Password reset link sent to your email"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User doesnot exsists with this Email"}, status = status.HTTP_400_BAD_REQUEST)
            
        if phone_number:
            return Response({"message":"Currently Reset password with phone number is not available"}, status = status.HTTP_400_BAD_REQUEST)
            try:
                validate_phone_number(phone_number)
            except ValidationError:
                return Response({"message": "Please provide a valid phone number"}, status = status.HTTP_400_BAD_REQUEST)
            phone_number = phone_number[3:]
            if User.objects.filter(phone_number = phone_number).exists():
                otp = random.randint(100000, 999999)
                cache.set(f"reset_otp:{phone_number}", otp, timeout = 600)
                message = f"your otp: {otp}"
                send_sms(phone_number, message)
                return Response({"message":"OTP send successfully"}, status = status.HTTP_200_OK)
            return Response({"message":"User with this phone number doesn't exsist"}, status = status.HTTP_400_BAD_REQUEST)
        
class ResetPasswordVerifyAPI(APIView):
    """
    Verify user new pasword is valid or not.

    Args:
        "email":use email
        token : reset password email token
        new password : user new password
    """
    
    def post(self, request):
        email = request.data.get('email',None)
        token = request.data.get('token', None)
        new_password = request.data.get('new_password', None)
        
        if not (email and token and new_password):
            return Response(
                {
                    "message" : "Email, Token and New password is required",
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        cached_token = cache.get(f"reset_token:{email}")
        if not cached_token or str(cached_token) != str(token):
            return Response(
                {
                    "message":"Invalid or Expired token"
                }, status = status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response(
                {
                    "message":"User with Email is not found",
                }, status = status.HTTP_400_BAD_REQUEST
            )
        user.password = make_password(new_password)
        user.save()
        
        cache.delete(f"reset_token:{email}")
        return Response(
            {
                "message":"Password Updated"
            }, status = status.HTTP_200_OK
        )
                
            
                
            
        
        