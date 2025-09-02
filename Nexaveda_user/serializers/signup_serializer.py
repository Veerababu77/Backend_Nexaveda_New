"""Validate new user details and add user"""

import uuid
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from utils.helper import generate_unique_username

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True, required = True)
    password2 = serializers.CharField(write_only = True, required = True)
    username = serializers.CharField(required = False)
    
    class Meta:
        model = User
        fields = ['id','username', 'phone_number', 'email', 'password','password2', 'role']
        
    def validate(self, attrs):
        if attrs['email'] == None:
            raise ValidationError({'email': 'Email required for user creation'})
        if attrs['password'] != attrs['password2']:
            raise ValidationError({'Password': 'Passwords must be same'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2', None)
        if not validated_data.get('username'):
            name_or_email = validated_data.get('name') or validated_data.get('email')
            validated_data['username'] = generate_unique_username(name_or_email)
        if validated_data.get('role') == "ADMIN":
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        return user
    