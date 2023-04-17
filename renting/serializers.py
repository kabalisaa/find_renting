from rest_framework import serializers
from .models import Province, District, Sector, Cell, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()
    class Meta:
        model = District
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()
    class Meta:
        model = Sector
        fields = '__all__'


class CellSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    class Meta:
        model = Cell
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    province = ProvinceSerializer()
    district = DistrictSerializer()
    sector = SectorSerializer()
    class Meta:
        model = Manager
        fields = '__all__'


class LandlordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    province = ProvinceSerializer()
    district = DistrictSerializer()
    sector = SectorSerializer()
    cell = CellSerializer()
    class Meta:
        model = Landlord
        fields = '__all__'


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField()
    property_type = PropertyTypeSerializer()
    province = ProvinceSerializer()
    district = DistrictSerializer()
    sector = SectorSerializer()
    cell = CellSerializer()
    images = PropertyImagesSerializer(many=True)
    class Meta:
        model = Property
        fields = '__all__'
class PublishingPaymentSerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField()
    property = PropertySerializer()
    class Meta:
        model = PublishingPayment
        fields = '__all__'


class GetInTouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetInTouch
        fields = ['id', 'first_name', 'last_name', 'email', 'subject', 'message', 'is_read', 'created_date']
        read_only_fields = ['id', 'created_date', 'is_read']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'full_name', 'rating', 'message', 'is_confirmed', 'created_date']
        read_only_fields = ['id', 'created_date', 'is_confirmed']