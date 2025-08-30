"""
Login API with username, phone number or email with password. 
"""
from Nexaveda_user.models.user_model import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from Nexaveda_user.serializers.login_serializer import LoginSerializer

class LoginAPI(APIView):
    def post(self,request):
        """
        function to take credientials as parameters and validate them.
        """
        serializer = LoginSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh' : str(refresh)
            },
            status = status.HTTP_200_OK
        )
        
        
    