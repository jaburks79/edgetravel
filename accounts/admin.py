from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class EdgeTravelUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'countries_visited',
        'is_verified_traveler', 'is_active', 'created_at'
    ]
    list_filter = ['is_verified_traveler', 'is_active', 'is_staff']
    search_fields = ['username', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('EdgeTravel Profile', {
            'fields': (
                'bio', 'countries_visited', 'is_verified_traveler',
                'allow_anonymous_posts', 'show_email', 'avatar',
                'location', 'website', 'last_ip',
            )
        }),
    )
