from django.apps import AppConfig


class NexavedaUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Nexaveda_user'
    
    def ready(self):
        import Nexaveda_user.signals
