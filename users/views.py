from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UserSerializer

from renting.models import UserLocation
from renting.serializers import UserLocationSerializer

User = get_user_model()


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        user_pk = self.kwargs.get('user_pk')

        if user_pk:
            queryset = queryset.filter(pk=user_pk)
        return queryset


class UserLocationViewSet(viewsets.ModelViewSet):
    serializer_class = UserLocationSerializer
    # queryset = UserLocation.objects.all()

    def get_queryset(self):
        queryset = UserLocation.objects.all()
        user_pk = self.kwargs.get('user_pk')
        location_pk = self.kwargs.get('location_pk')

        if user_pk and location_pk:
            queryset = queryset.filter(user__pk=user_pk, 
                                       pk=location_pk)
        return queryset