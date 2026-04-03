from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'risk_level', 'is_published', 'last_verified', 'report_count']
    list_filter = ['risk_level', 'region', 'is_published']
    search_fields = ['name', 'summary']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['risk_level', 'is_published']
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'region', 'country_code', 'risk_level', 'emoji_icon')}),
        ('Content', {'fields': ('summary', 'overview', 'safety_brief')}),
        ('Practical Info', {
            'classes': ('collapse',),
            'fields': ('visa_info', 'transport_info', 'money_info', 'connectivity_info', 'tips'),
        }),
        ('Media', {'fields': ('hero_image',)}),
        ('Publishing', {'fields': ('is_published', 'last_verified', 'created_by')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
