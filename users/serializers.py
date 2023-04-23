from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from renting.serializers import UserLocationSerializer, LandlordSerializer, ManagerSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    location = UserLocationSerializer(read_only=True)
    landlord_profile = LandlordSerializer(read_only=True)
    manager_profile = ManagerSerializer(read_only=True)

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name","email","is_manager","is_landlord","password","password_confirmation","manager_profile","landlord_profile","location"]
        extra_kwargs = {
            'password': {'write_only': True,'required': True},
            'password_confirmation': {'write_only': True,'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email address is already in use."))
        return value

    def validate(self, data):
        if data['password'] != data.pop('password_confirmation'):
            raise serializers.ValidationError(_("The passwords do not match."))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user