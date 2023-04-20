from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import DistrictFilter, SectorFilter, CellFilter
from .models import (Province, District, Sector, Cell, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial)
from .serializers import (ProvinceSerializer, DistrictSerializer, SectorSerializer, CellSerializer, ManagerSerializer, LandlordSerializer, PropertyTypeSerializer, PropertySerializer, PropertyImagesSerializer, PublishingPaymentSerializer, GetInTouchSerializer, TestimonialSerializer)

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistrictFilter

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectorFilter

    def list(self, request, *args, **kwargs):
        district_id = request.query_params.get('district')
        if district_id:
            queryset = self.queryset.filter(district_id=district_id)
        else:
            queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CellFilter

    def list(self, request, *args, **kwargs):
        sector_id = request.query_params.get('sector')
        if sector_id:
            queryset = self.queryset.filter(sector_id=sector_id)
        else:
            queryset = self.queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['province', 'district', 'sector', 'cell']
    search_fields = ['title', 'description']
    ordering_fields = ['renting_price']

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        property_obj = self.get_object()
        serializer = PropertyImagesSerializer(property_obj.images.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        province = self.request.query_params.get('province', None)
        district = self.request.query_params.get('district', None)
        sector = self.request.query_params.get('sector', None)
        cell = self.request.query_params.get('cell', None)

        if province:
            queryset = queryset.filter(province=province)
        if district:
            queryset = queryset.filter(district=district)
        if sector:
            queryset = queryset.filter(sector=sector)
        if cell:
            queryset = queryset.filter(cell=cell)

        return queryset


class PropertyImagesViewSet(viewsets.ModelViewSet):
    queryset = PropertyImages.objects.all()
    serializer_class = PropertyImagesSerializer

class PublishingPaymentViewSet(viewsets.ModelViewSet):
    queryset = PublishingPayment.objects.all()
    serializer_class = PublishingPaymentSerializer

class GetInTouchViewSet(viewsets.ModelViewSet):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
