# from django.urls import path, include
# from rest_framework_nested import routers

# from.views import UserViewSet, UserLocation
# from renting.views import ManagerViewSet, LandlordViewSet, PropertyViewSet, PropertyImagesViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')

# profile_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
# profile_router.register(r'manager', ManagerViewSet, basename='manager')
# profile_router.register(r'landlord', LandlordViewSet, basename='landlord')
# # profile_router.register(r'location', UserLocation, basename='location')

# # property_router = routers.NestedSimpleRouter(router, r'landlord', lookup='landlord')
# # property_router.register(r'properties', PropertyViewSet, basename='property')

# # property_image_router = routers.NestedSimpleRouter(router, r'properties', lookup='property')
# # property_image_router.register(r'images', PropertyImagesViewSet, basename='image')


# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(profile_router.urls)),
#     # path('', include(property_router.urls)),
#     # path('', include(property_image_router.urls)),
# ]
from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    UserViewSet,
    UserLocationViewSet,
)
from renting.views import (
    ManagerViewSet,
    LandlordViewSet,
    PropertyViewSet, 
    PropertyImagesViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

profile_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
profile_router.register(r'manager', ManagerViewSet, basename='manager')
profile_router.register(r'landlord', LandlordViewSet, basename='landlord')
profile_router.register(r'location', UserLocationViewSet, basename='location')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(profile_router.urls)),
]