# urls.py

from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    ProvinceViewSet,
    DistrictViewSet,
    SectorViewSet,
    CellViewSet,
    ManagerViewSet,
    LandlordViewSet,
    PropertyTypeViewSet,
    PropertyViewSet,
    PropertyImagesViewSet,
    PublishingPaymentViewSet,
    GetInTouchViewSet,
    TestimonialViewSet
)

router = routers.DefaultRouter()
router.register(r'managers', ManagerViewSet)
router.register(r'landlords', LandlordViewSet)
router.register(r'get_in_touch', GetInTouchViewSet)
router.register(r'testimonials', TestimonialViewSet)

# start location
router.register(r'provinces', ProvinceViewSet, basename='province')

province_router = routers.NestedSimpleRouter(router, r'provinces', lookup='province')
province_router.register(r'districts', DistrictViewSet, basename='district')

district_router = routers.NestedSimpleRouter(province_router, r'districts', lookup='district')
district_router.register(r'sectors', SectorViewSet, basename='sector')

sector_router = routers.NestedSimpleRouter(district_router, r'sectors', lookup='sector')
sector_router.register(r'cells', CellViewSet, basename='cell')
# end location


# start property
router.register(r'property_types', PropertyTypeViewSet, basename='property_type')

property_type_router = routers.NestedSimpleRouter(router, r'property_types', lookup='property_type')
property_type_router.register(r'properties', PropertyViewSet, basename='property')

property_router = routers.NestedSimpleRouter(property_type_router, r'properties', lookup='property')
property_router.register(r'images', PropertyImagesViewSet, basename='image')
property_router.register(r'publishing_payments', PublishingPaymentViewSet, basename='publishing_payment')
# end property

urlpatterns = [
    path('', include(router.urls)),
    path('', include(province_router.urls)),
    path('', include(district_router.urls)),
    path('', include(sector_router.urls)),
    path('', include(property_type_router.urls)),
    path('', include(property_router.urls)),
]
