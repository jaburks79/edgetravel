from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Destination(models.Model):
    """A high-risk travel destination with risk ratings and practical info."""

    RISK_LEVELS = [
        (1, 'Low'),
        (2, 'Moderate'),
        (3, 'Elevated'),
        (4, 'High'),
        (5, 'Extreme'),
    ]

    REGIONS = [
        ('middle_east', 'Middle East'),
        ('east_africa', 'East Africa'),
        ('west_africa', 'West Africa'),
        ('north_africa', 'North Africa'),
        ('central_africa', 'Central Africa'),
        ('south_asia', 'South Asia'),
        ('central_asia', 'Central Asia'),
        ('southeast_asia', 'Southeast Asia'),
        ('eastern_europe', 'Eastern Europe'),
        ('south_america', 'South America'),
        ('central_america', 'Central America'),
        ('oceania', 'Oceania'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    region = models.CharField(max_length=50, choices=REGIONS)
    country_code = models.CharField(max_length=3, blank=True, help_text="ISO 3166-1 alpha-2")
    risk_level = models.IntegerField(choices=RISK_LEVELS, default=3)

    # Content
    summary = models.TextField(max_length=500, help_text="Brief description shown on cards")
    overview = models.TextField(help_text="Detailed destination overview")
    safety_brief = models.TextField(help_text="Current safety situation and risks")
    visa_info = models.TextField(blank=True, help_text="Visa and entry requirements")
    transport_info = models.TextField(blank=True, help_text="How to get there and get around")
    money_info = models.TextField(blank=True, help_text="Currency, ATMs, costs")
    connectivity_info = models.TextField(blank=True, help_text="Phone, internet, SIM cards")
    tips = models.TextField(blank=True, help_text="Practical tips and advice")

    # Media
    hero_image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    emoji_icon = models.CharField(max_length=10, default='🌍')

    # Meta
    is_published = models.BooleanField(default=False)
    last_verified = models.DateField(
        null=True, blank=True,
        help_text="When the info was last verified as current"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, related_name='destinations_created'
    )

    class Meta:
        db_table = 'edgetravel_destinations'
        ordering = ['-risk_level', 'name']

    def __str__(self):
        return f"{self.name} (Risk: {self.get_risk_level_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'slug': self.slug})

    @property
    def risk_color(self):
        colors = {1: '#4ade80', 2: '#4ade80', 3: '#facc15', 4: '#f97316', 5: '#ef4444'}
        return colors.get(self.risk_level, '#888')

    @property
    def report_count(self):
        from reports.models import TripReport
        return TripReport.objects.filter(
            destination=self, is_approved=True
        ).count()
