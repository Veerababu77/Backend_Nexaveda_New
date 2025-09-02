import uuid
from django.contrib.auth import get_user_model
from django.db import models
from twilio.rest import Client
from django.conf import settings

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

class TimeStampModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True
        
def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body = message,
        from_ = settings.TWILIO_PHONE_NUMBER,
        to = phone_number
    )
    return message.sid
    
    
    