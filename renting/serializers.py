from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
# hyperlinks for nested relations on API
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from .models import Province, District, Sector, Cell, UserLocation, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial


class CellSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'sector_pk': 'sector__pk',
        'district_pk': 'sector__district__pk',
        'province_pk': 'sector__district__province__pk',
    }
    class Meta:
        model = Cell
        fields = ['id','cell_name']

class SectorSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'district_pk': 'sector__district__pk',
        'province_pk': 'sector__district__province__pk',
    }
    cells=CellSerializer(many=True, read_only=True)
    class Meta:
        model = Sector
        fields = ['id','sector_name','cells']

class DistrictSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'province_pk': 'district__province__pk',
    }
    province = serializers.StringRelatedField(read_only=True)
    sectors=SectorSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ['id','province','district_name','sectors',]

class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    districts=DistrictSerializer(many=True, read_only=True)
    class Meta:
        model = Province
        fields = [ 'id', 'province_name', 'districts',]

class UserLocationSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'location_pk': 'location__pk',
        'user_pk': 'user__pk',
    }
    user = serializers.StringRelatedField(read_only=True)
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    class Meta:
        model = UserLocation
        fields = ['id','user','province','district','sector']
        read_only_fields = ['user']

class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'manager_pk': 'manager__pk',
        'user_pk': 'user__pk',
    }
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Manager
        fields = ['id','user','gender','phone_number','profile_image',]
        read_only_fields = ['user']
    
    def update_or_create(self, *args, **kwargs):
        manager = Manager.objects.update_or_create(*args, **kwargs)
        return manager


class PropertyImagesSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'property_pk': 'property__pk',
        'landlord_pk': 'landlord__pk',
        'user_pk': 'landlord__user__pk',
    }
    property = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = PropertyImages
        fields = ['id','property','property_image']

class PropertyTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PropertyType
        fields = [ 'id', 'type_name',]

class PropertySerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'landlord_pk': 'landlord__pk',
        'user_pk': 'landlord__user__pk',
    }
    landlord = serializers.StringRelatedField(read_only=True)
    property_type=PropertyTypeSerializer()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    cell = serializers.StringRelatedField()
    images = PropertyImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = ['id','landlord','property_type','title','description','bedrooms','bathrooms','is_furnished','floors','plot_size','renting_price','status','status','province','district','sector','cell','street','pub_date','created_date','images']

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        property_obj = Property.objects.create(**validated_data)
        for image_data in images_data.values():
            PropertyImages.objects.create(property=property_obj, image=image_data)
        return property_obj

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data:
            instance.images.all().delete()
            for image_data in images_data.values():
                PropertyImages.objects.create(property=instance, image=image_data)

        return instance

class PublishingPaymentSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'property_pk': 'property__pk',
        'property_type_pk': 'property__property_type__pk',
    }
    landlord = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = PublishingPayment
        fields = ['id','property','landlord','payment_amount','payment_method','created_date']
        # read_only_fields = ['property','landlord','created_date']

class LandlordSerializer(serializers.HyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'landlord_pk': 'landlord__pk',
        'user_pk': 'user__pk',
    }
    user = serializers.StringRelatedField(read_only=True)
    properties=PropertySerializer(many=True, read_only=True)
    class Meta:
        model = Landlord
        fields = ['id',"user","gender","phone_number","profile_image","properties",]
        read_only_fields = ['user']

class GetInTouchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GetInTouch
        fields = [ 'id', 'first_name', 'last_name', 'email', 'subject', 'message', 'is_read', 'created_date']

class TestimonialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Testimonial
        fields = [ 'id', 'full_name', 'rating', 'message', 'is_confirmed', 'created_date']
        read_only_fields = ['id', 'created_date', 'is_confirmed']


class RentalSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,read_only=True)
    landlord = LandlordSerializer(required=False,read_only=True)
    property_type = serializers.CharField(required=False, allow_blank=True)
    bedrooms = serializers.IntegerField(required=False)
    bathrooms = serializers.IntegerField(required=False)
    is_furnished = serializers.BooleanField(required=False)
    floors = serializers.IntegerField(required=False)
    renting_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    district = serializers.CharField(required=False, allow_blank=True)
    sector = serializers.CharField(required=False, allow_blank=True)
    cell = serializers.CharField(required=False, allow_blank=True)
    images = PropertyImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = ['id','landlord','property_type','title','description','bedrooms','bathrooms','is_furnished','floors','plot_size','renting_price','status','province','district','sector','cell','street','images']
