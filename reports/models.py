from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class TripReport(models.Model):
    """User-submitted trip reports with voting and moderation."""

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='trip_reports'
    )
    destination = models.ForeignKey(
        'destinations.Destination', on_delete=models.CASCADE,
        related_name='trip_reports'
    )
    post_anonymously = models.BooleanField(
        default=False,
        help_text="Hide your username on this report"
    )

    # Trip details
    trip_start = models.DateField(null=True, blank=True)
    trip_end = models.DateField(null=True, blank=True)
    travel_style = models.CharField(max_length=50, choices=[
        ('solo', 'Solo'),
        ('partner', 'With Partner'),
        ('group', 'Small Group'),
        ('guided', 'Guided Tour'),
        ('journalism', 'Journalism/Work'),
    ], default='solo')

    # Content
    body = models.TextField(help_text="Your full trip report")
    tips = models.TextField(blank=True, help_text="Key tips for others")
    safety_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=3,
        help_text="How safe did you feel? 1=very unsafe, 5=very safe"
    )

    # Engagement
    upvotes = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    # Moderation
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    moderation_note = models.TextField(blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'edgetravel_trip_reports'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:280]
            slug = base_slug
            counter = 1
            while TripReport.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'slug': self.slug})

    @property
    def display_author(self):
        if self.post_anonymously:
            return "Anonymous Traveler"
        return self.author.username

    @property
    def trip_duration(self):
        if self.trip_start and self.trip_end:
            delta = self.trip_end - self.trip_start
            return delta.days
        return None


class ReportVote(models.Model):
    """Track who voted on what to prevent duplicate votes."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report = models.ForeignKey(TripReport, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'edgetravel_report_votes'
        unique_together = ['user', 'report']


class ReportComment(models.Model):
    """Comments on trip reports."""
    report = models.ForeignKey(TripReport, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    post_anonymously = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'edgetravel_report_comments'
        ordering = ['created_at']

    @property
    def display_author(self):
        if self.post_anonymously:
            return "Anonymous Traveler"
        return self.author.username
