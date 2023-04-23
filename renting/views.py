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


class ManagerViewSet(mixins.ListModelMixin, 
                     mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        queryset = Manager.objects.all()
        user_pk = self.kwargs.get('user_pk')
        manager_pk = self.kwargs.get('manager_pk')

        if user_pk:
            queryset = queryset.filter(user__pk=user_pk)
        elif user_pk and manager_pk:
            queryset = queryset.filter(pk=manager_pk, 
                                       user__pk=user_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LandlordViewSet(mixins.ListModelMixin, 
                      mixins.RetrieveModelMixin, 
                      viewsets.GenericViewSet):
    serializer_class = LandlordSerializer

    def get_queryset(self):
        queryset = Landlord.objects.all()
        user_pk = self.kwargs.get('user_pk')
        landlord_pk = self.kwargs.get('landlord_pk')

        if user_pk:
            queryset = queryset.filter(user__pk=user_pk)
        elif user_pk and landlord_pk:
            queryset = queryset.filter(pk=landlord_pk, 
                                       user__pk=user_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProvinceViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DistrictViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
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

class SectorViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = SectorSerializer

    def get_queryset(self):
        queryset = Sector.objects.all()
        province_pk = self.kwargs.get('province_pk')
        district_pk = self.kwargs.get('district_pk')
        
        if province_pk and district_pk:
            queryset = queryset.filter(district__province__pk=province_pk, 
                                       district__pk=district_pk)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CellViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
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
    serializer_class = PropertySerializer
    
    def get_queryset(self):
        queryset = Property.objects.all()
        property_type_pk = self.kwargs.get('property_type_pk')
        property_pk = self.kwargs.get('property_pk')
        landlord_pk = self.kwargs.get('landlord_pk')
        user_pk = self.kwargs.get('user_pk')

        if property_type_pk and property_pk:
            queryset = queryset.filter(property__pk=property_pk, 
                                       property__property_type__pk=property_type_pk)
        elif user_pk and landlord_pk and property_pk:
            queryset = queryset.filter(property__pk=property_pk, 
                                       property__landlord__pk=landlord_pk, 
                                       property__landlord__user__pk=user_pk)
        return queryset


class PropertyImagesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    serializer_class = PropertyImagesSerializer

    def get_queryset(self):
        queryset = PropertyImages.objects.all()
        landlord_pk = self.kwargs.get('landlord_pk')
        property_pk = self.kwargs.get('property_pk')
        property_type_pk = self.kwargs.get('property_type_pk')
        user_pk = self.kwargs.get('user_pk')
        if property_type_pk and property_pk:
            queryset = queryset.filter(property__pk=property_pk, 
                                       property__property_type__pk=property_type_pk)
        elif user_pk and landlord_pk and property_pk:
            queryset = queryset.filter(property__pk=property_pk, 
                                       property__landlord__pk=landlord_pk, 
                                       property__landlord__user__pk=user_pk)
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


class GetInTouchViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer


class TestimonialViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
