"""Sign up API for new user account creation."""

from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from Nexaveda_user.serializers.signup_serializer import SignupSerializer

User = get_user_model()

class SignupAPI(APIView):
    """Class based view for signup r register new user"""
    
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response(
            {
                "message":"User created successfully",
                "user" : {
                    "id" : user.id,
                    "username" : user.username,
                    "phone_number" : user.phone_number
                }
            }, status = status.HTTP_201_CREATED,
        )
        
        
        