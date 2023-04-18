from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url","id", "first_name", "last_name","email","password"]
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
