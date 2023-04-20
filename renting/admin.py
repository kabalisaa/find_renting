from django.contrib import admin
from renting.models import *


# Register your models here.
class LandlordInline(admin.StackedInline):
    model = Landlord

class ManagerInline(admin.StackedInline):
    model = Manager

class UserLocationInline(admin.StackedInline):
    model = UserLocation

class PropertyImageInline(admin.StackedInline):
    model = PropertyImages
    extra = 0

class PropertyInline(admin.StackedInline):
    model = Property
    inlines = [PropertyImageInline]
    extra = 0


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'province', 'district', 'sector','cell',)
    list_filter = ('province', 'district',)
    fieldsets = (
        ('LANDLORD INFO', {'fields': ('user', 'province', 'district','sector','cell',)}),
    )
    add_fieldsets = (
        ('REGISTER LANDLORD', {'fields': ('user', 'province', 'district','sector','cell',)}),
    )
    search_fields = ('user',)
    ordering = ('user',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone_number', 'image',)
    list_filter = ('gender',)
    fieldsets = (
        ('LANDLORD INFO', {'fields': ('user', 'gender', 'phone_number','profile_image',)}),
    )
    add_fieldsets = (
        ('REGISTER LANDLORD', {'fields': ('user', 'gender', 'phone_number','profile_image',)}),
    )
    search_fields = ('user',)
    ordering = ('user',)

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone_number', 'image',)
    list_filter = ('gender',)
    fieldsets = (
        ('LANDLORD INFO', {'fields': ('user', 'gender', 'phone_number','profile_image',)}),
    )
    add_fieldsets = (
        ('REGISTER LANDLORD', {'fields': ('user', 'gender', 'phone_number','profile_image',)}),
    )
    search_fields = ('user',)
    ordering = ('user__email',)
    inlines = [PropertyInline]


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    fieldsets = (
        ('PROPERTY TYPE', {'fields': ('type_name',)}),
    )
    add_fieldsets = (
        ('NEW PROPERTY TYPE', {
            'classes': ('wide',),
            'fields': ('type_name',),
        }),
    )
    search_fields = ('type_name',)
    ordering = ('type_name',)
    inlines = [PropertyInline]



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title','description','renting_price','bedrooms','bathrooms','floors','is_furnished', 'status', 'created_date',)
    list_filter = ('district','property_type','bedrooms','bathrooms','floors','is_furnished',)
    fieldsets = (
        ('PROPERTY DETAILS', {'fields': ('property_type','title','description',('bedrooms','bathrooms','floors','is_furnished'),'plot_size','renting_price','status',)}),
        ('Location Address', {'fields': ('province', 'district', 'sector', 'cell', 'street',)}),
        ('Property Owner', {'fields': ('landlord',)}),
    )
    add_fieldsets = (
        ('Property Owner', {'fields': ('landlord',)}),
        ('NEW PROPERTY', {'fields': ('property_type','title','description',('bedrooms','bathrooms','floors','is_furnished'),'plot_size','renting_price','status',)}),
        ('Location Address', {'fields': ('province', 'district', 'sector', 'cell', 'street',)}),
    )
    search_fields = ('landlord','title',)
    ordering = ('property_type','district',)
    inlines = [PropertyImageInline]


@admin.register(PropertyImages)
class PropertyImagesAdmin(admin.ModelAdmin):
    list_display = ('property','rental_image',)
    list_filter = ('property',)
    fieldsets = (
        ('PROPERTY IMAGES', {'fields': ('property',)}),
        (None, {'fields': ('property_image',)}),
    )
    add_fieldsets = (
        ('Property', {'fields': ('property',)}),
        ('Image', {'fields': ('property_image',)}),
    )
    search_fields = ('property',)
    ordering = ('property',)


@admin.register(PublishingPayment)
class PublishingPaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'landlord', 'payment_amount', 'payment_method','created_date',)
    list_filter = ('property', 'landlord', 'payment_method',)
    fieldsets = (
        ('PUBLISHED PAYMENT', {'fields': ('property', 'landlord', 'payment_amount', 'payment_method',)}),
    )
    add_fieldsets = (
        ('NEW PUBLISHED PAYMENT', {
            'classes': ('wide',),
            'fields': ('property', 'landlord', 'payment_amount', 'payment_method',),
        }),
    )
    search_fields = ('property', 'landlord', 'payment_method',)
    ordering = ('payment_method',)


class DistrictInline(admin.TabularInline):
    model = District
    extra = 0
@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('province_name',)
    fieldsets = (
        ('PROVINCE', {'fields': ('province_name',)}),
    )
    add_fieldsets = (
        ('NEW PROVINCE', {'fields': ('province_name',)}),
    )
    search_fields = ('province_name',)
    ordering = ('province_name',)
    inlines = [
        DistrictInline,
    ]

class SectorInline(admin.TabularInline):
    model = Sector
    extra = 0
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_name','province',)
    list_filter = ('province',)
    fieldsets = (
        ('DISTRICT', {'fields': ('province','district_name',)}),
    )
    add_fieldsets = (
        ('NEW DISTRICT', {'fields': ('province','district_name',)}),
    )
    search_fields = ('province','district_name',)
    ordering = ('province',)
    inlines = [
        SectorInline,
    ]


class CellInline(admin.TabularInline):
    model = Cell
    extra = 0
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector_name','district',)
    list_filter = ('district',)
    fieldsets = (
        ('SECTOR', {'fields': ('district','sector_name',)}),
    )
    add_fieldsets = (
        ('NEW SECTOR', {'fields': ('district','sector_name',)}),
    )
    search_fields = ('district','sector_name',)
    ordering = ('district',)
    inlines = [
        CellInline,
    ]



@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('cell_name','sector',)
    list_filter = ('sector',)
    fieldsets = (
        ('CELL', {'fields': ('sector','cell_name',)}),
    )
    add_fieldsets = (
        ('NEW CELL', {'fields': ('sector','cell_name',)}),
    )
    search_fields = ('sector','cell_name',)
    ordering = ('sector',)





# sorting models
def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        # Retrieve the original list
        app_dict = self._build_app_dict(request, app_label)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models customably within each app.
        for app in app_list:
            if app['app_label'] == 'RENTING':
                ordering = {
                    'Manager': 1,
                    'Landlord': 2,
                    'UserLocation': 3,
                    'PropertyType': 4,
                    'Property': 5,
                    'PublishingPayment': 6,
                    'Province': 7,
                    'District': 8,
                    'Sector': 9,
                    'Cell': 10,
                }
                app['models'].sort(key=lambda x: ordering[x['name']])
               
        return app_list
    
    
admin.AdminSite.get_app_list = get_app_list