from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import RegistrationView,UserRetrieveUpdateAPIView,GetAllUserAPIView

urlpatterns = [
    path('token/refresh',TokenRefreshView.as_view(),name="refresh_token"),
    path('token/access',TokenObtainPairView.as_view(),name="access_token"),
    path('token/verify',TokenVerifyView.as_view(),name="verify_token"),
    path('register',RegistrationView.as_view(),name="register_user"),
    path('user',UserRetrieveUpdateAPIView.as_view(),name='login_user'),
    path('adminpanel/user',GetAllUserAPIView.as_view(),name='get_users_admin'),
]
