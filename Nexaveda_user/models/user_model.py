"""Override Django built-in User model using AbstractUser to add more fields to the Model."""

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from validators import validate_phone_number
from django.contrib.auth.base_user import BaseUserManager
    
class UserManager(BaseUserManager):
    """
    To manage User creation through user manager.
    """
    use_in_migration = True
    
    def create_user(self, email = None, username = None, phone_number = None, password = None, role= None, **extra_fields):
        """
        Create and save a regular user.
        At least one of email, username, or phone_number must be provided.
        """
        if not (email or phone_number or username):
            raise ValueError("User must have at least one identifier: email, username, or phone_number")
        
        if email:
            email = self.normalize_email(email)
        
        if not username:
            username = f"Nexa_{uuid.uuid4().hex[:4]}"
            
        if not role:
            role = "STUDENT"
            
        # extra_fields.setdefault('role', 'STUDENT')
        if role == "ADMIN":
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)
        elif role == "INSTRUCTOR":
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", False)
            extra_fields.setdefault("is_active", True)
        else: 
            extra_fields.setdefault("is_staff", False)
            extra_fields.setdefault("is_superuser", False)
            extra_fields.setdefault("is_active", True)
        
        user = self.model(email = email, username = username, phone_number = phone_number, role = role, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email=None, username=None, phone_number=None, password=None, **extra_fields):
        """
        Create and save a superuser.
        """
        extra_fields.setdefault("role", "ADMIN")
        return self.create_user(email=email, username=username, phone_number=phone_number, password=password, **extra_fields)
    
class User(AbstractUser):
    """Override Model of a django User to add more fields."""
    
    ROLE_CHOICES = [
        ("STUDENT", "STUDENT"),
        ("INSTRUCTOR", "INSTRUCTOR"),
        ("ADMIN", "ADMIN")
    ]
    
    id = models.UUIDField(default = uuid.uuid4, unique = True, editable = False, primary_key = True)
    role = models.CharField(max_length = 100, choices = ROLE_CHOICES, default = "STUDENT")
    phone_number = models.CharField(max_length = 15, validators = [validate_phone_number], unique = True, null = True, blank = True)
    parent_phone_number = models.CharField(max_length = 15, validators = [validate_phone_number], unique = True, null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    emergency_contact = models.CharField(max_length = 50, null = True, blank = True)
    address = models.TextField(null = True, blank = True)
    profile_pic = models.ImageField(upload_to = 'profile_pic/', blank = True, null = True)
    
    objects = UserManager()
    
    def __str__(self):
        """
        return string of a model.
        """
        return self.username
        

  
    
