from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Nexaveda_user.apis.login_api import LoginAPI
from Nexaveda_user.apis.signup_api import SignupAPI
from Nexaveda_user.apis.logout_api import LogoutAPI
from Nexaveda_user.apis.rest_password_api import ResetPasswordAPI, ResetPasswordVerifyAPI

from Nexaveda_user.apis.course_model_api import CourseAPI, CourseDetailAPI
from Nexaveda_user.apis.topic_api import TopicAPI, TopicDetailAPI
from Nexaveda_user.apis.subtopic_api import SubtopicAPI, SubtopicDetailAPI
from Nexaveda_user.apis.rating_api import RatingAPI

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
    
    #Course urls
    path('course/', CourseAPI.as_view(), name = 'course'),
    path('course/<uuid:id>/', CourseDetailAPI.as_view(), name = 'course-detail'),
    
    path('course/<uuid:course_id>/topic/', TopicAPI.as_view(), name = 'topic'),
    path('course/topic/<uuid:id>/', TopicDetailAPI.as_view(), name = "topic-detail"),
    
    path('course/topic/<uuid:topic_id>/subtopic/', SubtopicAPI.as_view(), name = 'subtopic'),
    path('course/topic/subtopic/<uuid:id>/', SubtopicDetailAPI.as_view(), name = 'sub-topic-detail'),
    
    path('course/<uuid:course_id>/rating/', RatingAPI.as_view(), name = 'rating'),
]


