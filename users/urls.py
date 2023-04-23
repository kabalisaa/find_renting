from django.urls import path, include
from rest_framework import routers
from .views import UserRegistrationView, UserActivateView, UserLoginView, UserPasswordResetView, UserPasswordResetConfirmView, UserViewSet, UserLogoutView

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'register/', UserRegistrationView.as_view(), name='user-register'),
    path(r'activate/<uidb64>/<token>/', UserActivateView.as_view(), name='user-activate'),
    path(r'login/', UserLoginView.as_view(), name='user-login'),
    path(r'logout/', UserLogoutView.as_view(), name='user-logout'),
    path(r'password_reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path(r'password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
