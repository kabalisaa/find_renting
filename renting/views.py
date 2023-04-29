from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import (
    Manager, Landlord, Province, District, Sector, Cell,
    PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial
)
from .serializers import (
    ManagerSerializer, LandlordSerializer, ProvinceSerializer, DistrictSerializer,
    SectorSerializer, CellSerializer, PropertyTypeSerializer, PropertySerializer,
    PropertyImagesSerializer, PublishingPaymentSerializer, GetInTouchSerializer,
    TestimonialSerializer,RentalSearchSerializer
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

class DistrictViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        queryset = District.objects.all()
        district_pk = self.kwargs.get('district_pk')

        if district_pk:
            queryset = queryset.filter(pk=district_pk)
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
        district_pk = self.kwargs.get('district_pk')
        
        if district_pk:
            queryset = queryset.filter(district__pk=district_pk)
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
        district_pk = self.kwargs.get('district_pk')
        sector_pk = self.kwargs.get('sector_pk')

        if district_pk and sector_pk:
            queryset = queryset.filter(sector__district_id=district_pk,
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
        property_pk = self.kwargs.get('property_pk')
        landlord_pk = self.kwargs.get('landlord_pk')
        user_pk = self.kwargs.get('user_pk')

        if property_pk:
            queryset = queryset.filter(property__pk=property_pk)
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
        user_pk = self.kwargs.get('user_pk')
        if property_pk:
            queryset = queryset.filter(property__pk=property_pk)
        elif user_pk and landlord_pk and property_pk:
            queryset = queryset.filter(property__pk=property_pk, 
                                       property__landlord__pk=landlord_pk, 
                                       property__landlord__user__pk=user_pk)
        return queryset

    def perform_create(self, serializer):
        property_pk = self.kwargs.get('property_pk')
        if property_pk:
            property_obj = get_object_or_404(Property, pk=property_pk)
            serializer.save(property=property_obj)

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


class PublishingPaymentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
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


class SearchRentalViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.all()
    serializer_class = RentalSearchSerializer

    @action(detail=False, methods=['post'])
    def search(self, request):
        serializer = RentalSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        queryset = self.get_queryset()
        if data.get('property_type'):
            queryset = queryset.filter(property_type=data['property_type'])
        if data.get('bedrooms'):
            queryset = queryset.filter(bedrooms=data['bedrooms'])
        if data.get('bathrooms'):
            queryset = queryset.filter(bathrooms=data['bathrooms'])
        if data.get('is_furnished'):
            queryset = queryset.filter(is_furnished=data['is_furnished'])
        if data.get('floors'):
            queryset = queryset.filter(floors=data['floors'])
        if data.get('plot_size'):
            queryset = queryset.filter(plot_size=data['plot_size'])
        if data.get('renting_price'):
            queryset = queryset.filter(renting_price=data['renting_price'])
        if data.get('district'):
            queryset = queryset.filter(district=data['district'])
        if data.get('sector'):
            queryset = queryset.filter(sector=data['sector'])
        if data.get('cell'):
            queryset = queryset.filter(cell=data['cell'])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)