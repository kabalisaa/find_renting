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
    user = serializers.StringRelatedField(read_only=True)
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    class Meta:
        model = UserLocation
        fields = ['id','user','province','district','sector']
        read_only_fields = ['user']

class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Manager
        fields = ['id','user','gender','phone_number','profile_image',]
        read_only_fields = ['user']


class PropertyImagesSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'property_pk': 'property__pk',
        'property_type_pk': 'property__property_type__pk',
    }
    property = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = PropertyImages
        fields = ['id','property','property_image']


class PropertySerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'property_type_pk': 'property_type__pk',
    }
    landlord = serializers.StringRelatedField(read_only=True)
    property_type=serializers.StringRelatedField()
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
    user = serializers.StringRelatedField(read_only=True)
    properties=PropertySerializer(many=True, read_only=True)
    class Meta:
        model = Landlord
        fields = ['id',"user","gender","phone_number","profile_image",'properties']
        read_only_fields = ['user']

class PropertyTypeSerializer(serializers.HyperlinkedModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    class Meta:
        model = PropertyType
        fields = [ 'id', 'type_name', 'properties']

class GetInTouchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GetInTouch
        fields = [ 'id', 'first_name', 'last_name', 'email', 'subject', 'message', 'is_read', 'created_date']

class TestimonialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Testimonial
        fields = [ 'id', 'full_name', 'rating', 'message', 'is_confirmed', 'created_date']
        read_only_fields = ['id', 'created_date', 'is_confirmed']