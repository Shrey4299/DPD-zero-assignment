from django.contrib import admin
from .models import RegisterUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.db import models

class UserAdminConfig(UserAdmin):
    model = RegisterUser
    search_fields = ('email', 'full_name', 'username')  # Change 'name' to 'username' here
    list_filter = ('is_active', 'is_staff',)
    ordering = ('-start_date',)
    list_display = ('email', 'full_name', 'username', 'phone_number', 'gender', 'age', 'is_active', 'is_staff')  # Include 'full_name', 'gender', 'age' in the list_display
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'username', 'phone_number', 'gender', 'age')}),  # Change 'name' to 'username' here
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'username', 'phone_number', 'gender', 'age', 'password1', 'password2', 'is_active', 'is_staff')}  # Change 'name' to 'username' here
         ),
    )

admin.site.register(RegisterUser, UserAdminConfig)
