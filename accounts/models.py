from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model for EdgeTravel community."""
    
    bio = models.TextField(max_length=1000, blank=True)
    countries_visited = models.PositiveIntegerField(default=0)
    is_verified_traveler = models.BooleanField(
        default=False,
        help_text="Verified by admin as an experienced high-risk traveler"
    )
    allow_anonymous_posts = models.BooleanField(
        default=False,
        help_text="When enabled, your posts can be displayed without your username"
    )
    show_email = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Security: track for suspicious activity
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'edgetravel_users'

    def __str__(self):
        return self.username

    @property
    def display_name(self):
        """Returns 'Anonymous Traveler' if user prefers anonymous posting."""
        if self.allow_anonymous_posts:
            return "Anonymous Traveler"
        return self.username

    @property
    def reputation(self):
        """Calculate user reputation based on contributions."""
        from reports.models import TripReport
        from forum.models import ForumPost
        report_votes = sum(
            r.upvotes for r in TripReport.objects.filter(author=self, is_approved=True)
        )
        post_count = ForumPost.objects.filter(author=self, is_approved=True).count()
        verified_bonus = 50 if self.is_verified_traveler else 0
        return report_votes + (post_count * 2) + verified_bonus
