from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Role

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('organization', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('organization', 'role')}),
    )
    list_display = ('username', 'email', 'organization', 'role')
    list_filter = ('organization', 'role')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Organization)
admin.site.register(Role)