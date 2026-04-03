from django.contrib import admin
from .models import Guide, GuideCategory


@admin.register(GuideCategory)
class GuideCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'author', 'read_count',
        'is_published', 'is_featured', 'published_at'
    ]
    list_filter = ['is_published', 'is_featured', 'category']
    search_fields = ['title', 'body', 'excerpt']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['read_count', 'created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'category', 'destination')}),
        ('Content', {'fields': ('excerpt', 'body', 'hero_image')}),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords'),
        }),
        ('Publishing', {'fields': (
            'is_published', 'is_featured', 'published_at',
            'read_count', 'created_at', 'updated_at',
        )}),
    )
