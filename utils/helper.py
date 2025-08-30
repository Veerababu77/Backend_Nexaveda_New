import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_unique_username(name_or_email):
    
    prefix = name_or_email.split('@')[0] if '@' in name_or_email else name_or_email
    prefix = prefix[:6]
    
    for i in range(10):
        suffix = uuid.uuid4().hex[:6]
        username = f"Nexa_{prefix}_{suffix}"
        if not User.objects.filter(username = username):
            return username
    
    raise ValueError("Unable to create unique username") 