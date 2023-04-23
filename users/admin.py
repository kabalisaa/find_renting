from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from renting.admin import UserLocationInline
from . forms import UserRegisterForm, UserUpdateForm, UpdatePasswordForm


User = get_user_model()

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_superuser',)
    list_filter = ('is_manager', 'is_landlord','is_active','is_superuser','date_joined',)
    list_editable = ()
    list_per_page = 10
    date_hierarchy = ('date_joined')
    fieldsets = (
        ('User Credentials', {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('User type', {'fields': ('is_manager', 'is_landlord',)}),
        ('Permissions', {'classes': ('collapse',),'fields': (('is_active', 'is_staff','is_superuser'),'groups', 'user_permissions',)}),
        ('Other Info', {'classes': ('collapse',),'fields': (('date_joined', 'last_login'),)}),
    )
    add_fieldsets = (
        ('REGISTER NEW USER', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',),
        }),
        (None, {
            'classes': ('wide',),
            'fields': (('is_manager', 'is_landlord',),),
        }),
        ('Create password', {
            'classes': ('wide',),
            'fields': ('password1', 'password2',),
        }),
        ('User permissions', {
            'classes': ('collapse',),
            'fields': (('is_active', 'is_staff','is_superuser'),'groups', 'user_permissions',),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email','date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [UserLocationInline]
