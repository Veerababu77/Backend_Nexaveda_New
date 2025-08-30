from django.urls import path
from rest_framewrok_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    #jwt authentication urls
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'refresh_token'),
    
]


