"""Login serializer to check the user is exsits or not."""

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    def validate(self, attrs):
        request = self.context.get('request')
        login = attrs.get('login')
        password = attrs.get('password')
        
        user = None
        
        try:
            user_obj = User.objects.get(
                (Q(email = login) | Q(phone_number = login) | Q(username = login))
            )
            user = authenticate(username = user_obj, password = password)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid Credentials")
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        attrs['user'] = user
        return attrs
            