from django.contrib import admin
from .models import ForumCategory, ForumPost, ForumReply, Feedback


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'icon']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'reply_count',
        'view_count', 'is_approved', 'is_pinned', 'is_hot', 'created_at'
    ]
    list_filter = ['is_approved', 'is_pinned', 'is_hot', 'is_locked', 'category']
    search_fields = ['title', 'body', 'author__username']
    list_editable = ['is_approved', 'is_pinned', 'is_hot']
    readonly_fields = ['reply_count', 'view_count', 'created_at']
    actions = ['pin_posts', 'lock_posts']

    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)
    pin_posts.short_description = "Pin selected posts"

    def lock_posts(self, request, queryset):
        queryset.update(is_locked=True)
    lock_posts.short_description = "Lock selected posts"


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    list_editable = ['is_approved']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']