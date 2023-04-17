from django.urls import path, include
from rest_framework import routers
from .views import ProvinceViewSet, DistrictViewSet, SectorViewSet, CellViewSet, ManagerViewSet, LandlordViewSet, PropertyTypeViewSet, PropertyViewSet, PropertyImagesViewSet, PublishingPaymentViewSet, GetInTouchViewSet, TestimonialViewSet

router = routers.DefaultRouter()
router.register(r'provinces', ProvinceViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'cells', CellViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'landlords', LandlordViewSet)
router.register(r'property_types', PropertyTypeViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'property_images', PropertyImagesViewSet)
router.register(r'publishing_payments', PublishingPaymentViewSet)
router.register(r'get_in_touch', GetInTouchViewSet)
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
