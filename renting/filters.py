import django_filters

from .models import Province, District, Sector, Cell


class DistrictFilter(django_filters.FilterSet):
    province = django_filters.CharFilter(field_name='province__province_name')

    class Meta:
        model = District
        fields = ['province']


class SectorFilter(django_filters.FilterSet):
    province = django_filters.CharFilter(field_name='district__province__province_name')
    district = django_filters.CharFilter(field_name='district__district_name')

    class Meta:
        model = Sector
        fields = ['province', 'district']


class CellFilter(django_filters.FilterSet):
    province = django_filters.CharFilter(field_name='sector__district__province__province_name')
    district = django_filters.CharFilter(field_name='sector__district__district_name')
    sector = django_filters.CharFilter(field_name='sector__sector_name')

    class Meta:
        model = Cell
        fields = ['province', 'district', 'sector']
