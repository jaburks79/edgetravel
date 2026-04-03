from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class GuideCategory(models.Model):
    """Categories for organizing guides."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'edgetravel_guide_categories'
        ordering = ['order', 'name']
        verbose_name_plural = 'Guide Categories'

    def __str__(self):
        return self.name


class Guide(models.Model):
    """Long-form articles and practical guides — the SEO engine."""

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='guides'
    )
    category = models.ForeignKey(
        GuideCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='guides'
    )
    destination = models.ForeignKey(
        'destinations.Destination', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='guides'
    )

    # Content
    excerpt = models.TextField(max_length=500, help_text="Preview shown in listings")
    body = models.TextField(help_text="Full guide content (Markdown supported)")
    hero_image = models.ImageField(upload_to='guides/', blank=True, null=True)

    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    # Stats
    read_count = models.PositiveIntegerField(default=0)

    # Publishing
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'edgetravel_guides'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:280]
            slug = base_slug
            counter = 1
            while Guide.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('guide_detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        word_count = len(self.body.split())
        return max(1, round(word_count / 250))
