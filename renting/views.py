from rest_framework import viewsets
from .models import (Province, District, Sector, Cell, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial)
from .serializers import (ProvinceSerializer, DistrictSerializer, SectorSerializer, CellSerializer, ManagerSerializer, LandlordSerializer, PropertyTypeSerializer, PropertySerializer, PropertyImagesSerializer, PublishingPaymentSerializer, GetInTouchSerializer, TestimonialSerializer)

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user!=obj.user:
            raise PermissionDenied(
                'You do not have permission to perform this action.'
            )
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        instance.delete()

class LandlordViewSet(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user!=obj.user:
            raise PermissionDenied(
                'You do not have permission to perform this action.'
            )
        serializer.save(user=self.request.user)
    def perform_destroy(self, instance):
        instance.delete()

class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    def get_queryset(self):
        return self.queryset.filter(landlord=self.request.user)
    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user.landlord)
    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user.landlord!=obj.landlord:
            raise PermissionDenied(
                'You do not have permission to perform this action.'
            )
        serializer.save(landlord=self.request.user.landlord)
    def perform_destroy(self, instance):
        instance.delete()

class PropertyImagesViewSet(viewsets.ModelViewSet):
    queryset = PropertyImages.objects.all()
    serializer_class = PropertyImagesSerializer

class PublishingPaymentViewSet(viewsets.ModelViewSet):
    queryset = PublishingPayment.objects.all()
    serializer_class = PublishingPaymentSerializer
    def get_queryset(self):
        return self.queryset.filter()
    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user.landlord)
    def perform_update(self, serializer):
        serializer.save(landlord=self.request.user.landlord)
    def perform_destroy(self, instance):
        instance.delete()

class GetInTouchViewSet(viewsets.ModelViewSet):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer
    def get_queryset(self):
        return self.queryset.filter()
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_destroy(self, instance):
        instance.delete()

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    def get_queryset(self):
        return self.queryset.filter(is_confirmed=True)
    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        serializer.save()
    def perform_destroy(self, instance):
        instance.delete()
