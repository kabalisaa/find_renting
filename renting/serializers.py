from rest_framework import serializers
from .models import Province, District, Sector, Cell, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial




class CellSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()
    class Meta:
        model = Cell
        fields = ['sector','cell_name']


class SectorSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()
    cells=CellSerializer(many=True)
    class Meta:
        model = Sector
        fields = ['district','sector_name','cells']


class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()
    sectors=SectorSerializer(many=True)
    class Meta:
        model = District
        fields = ['__all__']


class ProvinceSerializer(serializers.ModelSerializer):
    districts=DistrictSerializer(many=True)
    class Meta:
        model = Province
        fields = ['province_name', 'districts',]

class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    class Meta:
        model = Manager
        fields = ['user','gender','phone_number','province','district','sector','profile_image',]


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['type_name',]


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['property','property_image','images']


class PropertySerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField()
    property_type = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    cell = serializers.StringRelatedField()
    images = PropertyImagesSerializer(many=True)
    class Meta:
        model = Property
        fields = ['landlord','property_type','title','description','bedrooms','bathrooms','is_furnished','floors','plot_size','renting_price','status','status','province','district','sector','cell','street','pub_date','created_date','images']
class PublishingPaymentSerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField()
    property = serializers.StringRelatedField()
    class Meta:
        model = PublishingPayment
        fields = ['property','landlord','payment_amount','payment_method','created_date']

class LandlordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    cell =serializers.StringRelatedField()
    properties=PropertySerializer(many=True)
    payments=PublishingPaymentSerializer(many=True)
    class Meta:
        model = Landlord
        fields = ["user","gender","phone_number","province","district","sector","cell","profile_image",'properties','payments']

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