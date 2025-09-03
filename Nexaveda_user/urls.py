from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Nexaveda_user.apis.login_api import LoginAPI
from Nexaveda_user.apis.signup_api import SignupAPI
from Nexaveda_user.apis.logout_api import LogoutAPI
from Nexaveda_user.apis.rest_password_api import ResetPasswordAPI, ResetPasswordVerifyAPI

app_name = "Nexaveda_user"

urlpatterns = [
    #jwt authentication urls
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'refresh_token'),
    
    #loginurls
    path('login/', LoginAPI.as_view(), name = 'login'),
    #signup urls
    path('signup/', SignupAPI.as_view(), name = 'signup'),
    #logout urls
    path('logout/', LogoutAPI.as_view(), name = 'logout'),
    #reset password url
    path('reset-password/', ResetPasswordAPI.as_view(), name = 'reset_password'),
    path('reset-password-verify/', ResetPasswordVerifyAPI.as_view(), name = 'reset-password-verify'),
    
]


