from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class ForumCategory(models.Model):
    """Forum sections."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='◈')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'edgetravel_forum_categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Forum Categories'

    def __str__(self):
        return self.name

    @property
    def post_count(self):
        return self.posts.filter(is_approved=True).count()


class ForumPost(models.Model):
    """Forum discussion threads."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='forum_posts'
    )
    category = models.ForeignKey(
        ForumCategory, on_delete=models.CASCADE,
        related_name='posts'
    )
    body = models.TextField(max_length=20000)
    post_anonymously = models.BooleanField(default=False)

    # Engagement
    reply_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)

    # Moderation
    is_approved = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reply_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'edgetravel_forum_posts'
        ordering = ['-is_pinned', '-last_reply_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:280]
            slug = base_slug
            counter = 1
            while ForumPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum_post_detail', kwargs={'slug': self.slug})

    @property
    def display_author(self):
        if self.post_anonymously:
            return "Anonymous Traveler"
        return self.author.username


class ForumReply(models.Model):
    """Replies to forum posts."""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='forum_replies'
    )
    body = models.TextField(max_length=10000)
    post_anonymously = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'edgetravel_forum_replies'
        ordering = ['created_at']

    @property
    def display_author(self):
        if self.post_anonymously:
            return "Anonymous Traveler"
        return self.author.username

class Feedback(models.Model):
    """User feedback and suggestions."""
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=5000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'edgetravel_feedback'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} — {self.name or 'Anonymous'}"