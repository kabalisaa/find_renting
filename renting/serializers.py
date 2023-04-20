from rest_framework import serializers
from .models import Province, District, Sector, Cell, UserLocation, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial




class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['id','cell_name']


class SectorSerializer(serializers.ModelSerializer):
    cells=CellSerializer(many=True, read_only=True)
    class Meta:
        model = Sector
        fields = ['id','sector_name','cells']


class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(read_only=True)
    sectors=SectorSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ['id','province','district_name','sectors',]


class ProvinceSerializer(serializers.ModelSerializer):
    districts=DistrictSerializer(many=True, read_only=True)
    class Meta:
        model = Province
        fields = ['id','province_name', 'districts',]

class UserLocationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    class Meta:
        model = UserLocation
        fields = ['id','user','province','district','sector']
        read_only_fields = ['user']

class ManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Manager
        fields = ['id','user','gender','phone_number','profile_image',]
        read_only_fields = ['user']


class PropertyImagesSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = PropertyImages
        fields = ['id','property','property_image']
        read_only_fields = ['property']


class PropertySerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField(read_only=True)
    property_type=serializers.StringRelatedField()
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    cell = serializers.PrimaryKeyRelatedField(queryset=Cell.objects.all())
    images = PropertyImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = ['id','landlord','property_type','title','description','bedrooms','bathrooms','is_furnished','floors','plot_size','renting_price','status','status','province','district','sector','cell','street','pub_date','created_date','images']



class PublishingPaymentSerializer(serializers.ModelSerializer):
    landlord = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = PublishingPayment
        fields = ['id','property','landlord','payment_amount','payment_method','created_date']
        read_only_fields = ['property','landlord','created_date']

class LandlordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    properties=PropertySerializer(many=True, read_only=True)
    class Meta:
        model = Landlord
        fields = ['id',"user","gender","phone_number","profile_image",'properties']
        read_only_fields = ['user']


class PropertyTypeSerializer(serializers.ModelSerializer):
    properties = PropertyImagesSerializer(many=True, read_only=True)
    class Meta:
        model = PropertyType
        fields = ['id','type_name','properties']


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