from django.contrib import admin
from .models import TripReport, ReportComment, ReportVote


@admin.register(TripReport)
class TripReportAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'destination', 'travel_style',
        'upvotes', 'is_approved', 'is_featured', 'created_at'
    ]
    list_filter = ['is_approved', 'is_featured', 'travel_style', 'destination']
    search_fields = ['title', 'body', 'author__username']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['upvotes', 'comment_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_reports', 'feature_reports']

    def approve_reports(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} reports approved.')
    approve_reports.short_description = "Approve selected reports"

    def feature_reports(self, request, queryset):
        count = queryset.update(is_featured=True, is_approved=True)
        self.message_user(request, f'{count} reports featured.')
    feature_reports.short_description = "Feature selected reports"


@admin.register(ReportComment)
class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ['report', 'author', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    list_editable = ['is_approved']


@admin.register(ReportVote)
class ReportVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'report', 'created_at']
    readonly_fields = ['user', 'report', 'created_at']
