"""EdgeTravel URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from edgetravel.views import HomeView
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from edgetravel.sitemaps import DestinationSitemap, GuideSitemap, StaticSitemap

sitemaps = {
    'destinations': DestinationSitemap,
    'guides': GuideSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('accounts/', include('accounts.urls')),
    path('destinations/', include('destinations.urls')),
    path('reports/', include('reports.urls')),
    path('guides/', include('guides.urls')),
    path('forum/', include('forum.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
