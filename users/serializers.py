from django.contrib.auth import get_user_model

from rest_framework import serializers

from renting.serializers import UserLocationSerializer, LandlordSerializer, ManagerSerializer

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    location = UserLocationSerializer(read_only=True)
    landlord_profile = LandlordSerializer(read_only=True)
    manager_profile = ManagerSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["url","id", "first_name", "last_name","email","is_manager","is_landlord","password","manager_profile","landlord_profile","location"]
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
