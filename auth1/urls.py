from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.urls import path , include
from .views import *

urlpatterns = [
    path('register/' , RegisterAPI.as_view()),
    path('token/' , TokenObtainPairView.as_view() , name='token_obtain'),
    path('token/refresh/' , TokenRefreshView.as_view() , name='token_refresh'),
    path('delete-account/' , DeleteAccountAPI.as_view())
]