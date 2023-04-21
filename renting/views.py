from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import (
    Manager, Landlord, Province, District, Sector, Cell,
    PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial
)
from .serializers import (
    ManagerSerializer, LandlordSerializer, ProvinceSerializer, DistrictSerializer,
    SectorSerializer, CellSerializer, PropertyTypeSerializer, PropertySerializer,
    PropertyImagesSerializer, PublishingPaymentSerializer, GetInTouchSerializer,
    TestimonialSerializer
)


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class LandlordViewSet(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        queryset = Province.objects.all()
        province_pk = self.kwargs.get('province_pk')
        if province_pk:
            queryset = queryset.filter(pk=province_pk)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        queryset = District.objects.all()
        province_pk = self.kwargs.get('province_pk')
        
        if province_pk:
            queryset = queryset.filter(province=province_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SectorViewSet(viewsets.ModelViewSet):
    serializer_class = SectorSerializer

    def get_queryset(self):
        queryset = Sector.objects.all()
        province_pk = self.kwargs.get('province_pk')
        district_pk = self.kwargs.get('district_pk')
        
        if province_pk and district_pk:
            queryset = queryset.filter(district__province__pk=province_pk, district__pk=district_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CellViewSet(viewsets.ModelViewSet):
    serializer_class = CellSerializer
    
    def get_queryset(self):
        queryset = Cell.objects.all()
        province_pk = self.kwargs.get('province_pk')
        district_pk = self.kwargs.get('district_pk')
        sector_pk = self.kwargs.get('sector_pk')

        if province_pk and district_pk and sector_pk:
            queryset = queryset.filter(sector__district__province_id=province_pk, 
                                       sector__district_id=district_pk,
                                       sector_id=sector_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

    def get_queryset(self):
        if 'property_type_pk' in self.kwargs:
            return Property.objects.filter(property_type_id=self.kwargs['property_type_pk'])
        return self.queryset


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_queryset(self):
        if 'property_type_pk' in self.kwargs and 'property_pk' in self.kwargs:
            return PropertyImages.objects.filter(property_id=self.kwargs['property_pk'])
        elif 'property_type_pk' in self.kwargs:
            return self.queryset.filter(property_type_id=self.kwargs['property_type_pk'])
        return self.queryset


class PropertyImagesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    serializer_class = PropertyImagesSerializer

    def get_queryset(self):
        queryset = PropertyImages.objects.all()
        property_pk = self.kwargs.get('property_pk')
        property_type_pk = self.kwargs.get('property_type_pk')
        if property_pk:
            queryset = queryset.filter(property=property_pk)
        elif property_type_pk:
            queryset = queryset.filter(property__property_type=property_type_pk)
        return queryset

    def perform_create(self, serializer):
        property_pk = self.kwargs.get('property_pk')
        property_type_pk = self.kwargs.get('property_type_pk')
        if property_pk:
            property_obj = get_object_or_404(Property, pk=property_pk)
            serializer.save(property=property_obj)
        elif property_type_pk:
            property_type_obj = get_object_or_404(PropertyType, pk=property_type_pk)
            serializer.save(property=property_type_obj.property_set.first())

    @action(detail=True, methods=['POST'])
    def set_primary(self, request, pk=None, **kwargs):
        instance = self.get_object()
        instance.set_primary()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def unset_primary(self, request, pk=None, **kwargs):
        instance = self.get_object()
        instance.unset_primary()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PublishingPaymentViewSet(viewsets.ModelViewSet):
    queryset = PublishingPayment.objects.all()
    serializer_class = PublishingPaymentSerializer


class GetInTouchViewSet(viewsets.ModelViewSet):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
