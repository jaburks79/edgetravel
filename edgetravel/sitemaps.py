from django.contrib.sitemaps import Sitemap
from destinations.models import Destination
from guides.models import Guide


class DestinationSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Destination.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class GuideSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Guide.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return ['home', 'destination_list', 'report_list', 'guide_list', 'forum_home']

    def location(self, item):
        from django.urls import reverse
        return reverse(item)