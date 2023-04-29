# urls.py

from django.urls import path, include
from rest_framework_nested import routers

from .views import (
    DistrictViewSet,
    SectorViewSet,
    CellViewSet,
    SearchRentalViewSet,
    PropertyViewSet,
    PropertyImagesViewSet,
    PublishingPaymentViewSet,
    GetInTouchViewSet,
    TestimonialViewSet
)

router = routers.DefaultRouter()
router.register(r'find_renting', SearchRentalViewSet, basename='search_rental')
router.register(r'publishing_payments', PublishingPaymentViewSet, basename='publishing_payment')
router.register(r'get_in_touch', GetInTouchViewSet, basename='messages')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

# start location
router.register(r'districts', DistrictViewSet, basename='district')

district_router = routers.NestedSimpleRouter(router, r'districts', lookup='district')
district_router.register(r'sectors', SectorViewSet, basename='sector')

sector_router = routers.NestedSimpleRouter(district_router, r'sectors', lookup='sector')
sector_router.register(r'cells', CellViewSet, basename='cell')
# end location

urlpatterns = [
    path('', include(router.urls)),
    path('', include(district_router.urls)),
    path('', include(sector_router.urls)),
]
