from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers

from renting.views import (
    ManagerViewSet,
    LandlordViewSet,
    PropertyViewSet,
    PropertyImagesViewSet
)

from .views import (
    UserRegistrationView, 
    UserActivateView, 
    UserLoginView, 
    UserPasswordResetView, 
    UserPasswordResetConfirmView, 
    UserViewSet, 
    UserLogoutView,
    UserLocationViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

profile_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
profile_router.register(r'location', UserLocationViewSet, basename='location')
profile_router.register(r'manager', ManagerViewSet, basename='manager')
profile_router.register(r'landlord', LandlordViewSet, basename='landlord')

property_router = routers.NestedSimpleRouter(profile_router, r'landlord', lookup='landlord')
property_router.register(r'properties', PropertyViewSet, basename='property')

property_image_router = routers.NestedSimpleRouter(property_router, r'properties', lookup='property')
property_image_router.register(r'images', PropertyImagesViewSet, basename='image')

urlpatterns = [
    path(r'', include(router.urls)),
    path('', include(profile_router.urls)),
    path('', include(property_router.urls)),
    path('', include(property_image_router.urls)),
    path(r'register/', UserRegistrationView.as_view(), name='user-register'),
    path(r'activate/<uidb64>/<token>/', UserActivateView.as_view(), name='user-activate'),
    path(r'login/', UserLoginView.as_view(), name='user-login'),
    path(r'logout/', UserLogoutView.as_view(), name='user-logout'),
    path(r'password_reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path(r'password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
