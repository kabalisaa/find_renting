from rest_framework import serializers
from .models import Province, District, Sector, Cell, UserLocation, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial




class CellSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()
    class Meta:
        model = Cell
        fields = ['id','sector','cell_name']
        read_only_fields = ['sector']


class SectorSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()
    cells=CellSerializer(many=True)
    class Meta:
        model = Sector
        fields = ['id','district','sector_name','cells']
        read_only_fields = ['district']


class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()
    sectors=SectorSerializer(many=True)
    class Meta:
        model = District
        fields = ['id','province','sectors',]
        read_only_fields = ['province']


class ProvinceSerializer(serializers.ModelSerializer):
    districts=DistrictSerializer(many=True)
    class Meta:
        model = Province
        fields = ['id','province_name', 'districts',]

class UserLocationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    class Meta:
        model = UserLocation
        fields = ['id','user','province','district','sector']
        read_only_fields = ['user']

class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Manager
        fields = ['id','user','gender','phone_number','profile_image',]
        read_only_fields = ['user']


class PropertyImagesSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()
    class Meta:
        model = PropertyImages
        fields = ['id','property','property_image']
        read_only_fields = ['property']


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
        fields = ['id','landlord','property_type','title','description','bedrooms','bathrooms','is_furnished','floors','plot_size','renting_price','status','status','province','district','sector','cell','street','pub_date','created_date','images']
        read_only_fields = ['landlord','pub_date','created_date',]


class PropertyTypeSerializer(serializers.ModelSerializer):
    properties = PropertyImagesSerializer(many=True)
    class Meta:
        model = PropertyType
        fields = ['id','type_name','properties']



class PublishingPaymentSerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField()
    property = serializers.StringRelatedField()
    class Meta:
        model = PublishingPayment
        fields = ['id','property','landlord','payment_amount','payment_method','created_date']
        read_only_fields = ['property','landlord','created_date']

class LandlordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    properties=PropertySerializer(many=True)
    payments=PublishingPaymentSerializer(many=True)
    class Meta:
        model = Landlord
        fields = ['id',"user","gender","phone_number","profile_image",'properties','payments']
        read_only_fields = ['user']

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