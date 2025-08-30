from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Nexaveda_user.apis.login_api import LoginAPI


urlpatterns = [
    #jwt authentication urls
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'refresh_token'),
    
    #loginurls
    path('login/', LoginAPI.as_view(), name = 'login'),
    
]


