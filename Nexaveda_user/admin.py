from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from Nexaveda_user.models.user_model import User

class UserAdmin(BaseUserAdmin):
    # Fields to display in admin list
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    # Fields to use in the admin form for adding/changing users
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email','username')
    filter_horizontal = ('groups', 'user_permissions',)

# Register the custom user model with the admin
admin.site.register(User, UserAdmin)


