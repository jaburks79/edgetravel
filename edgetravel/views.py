from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from destinations.models import Destination
        from reports.models import TripReport
        from guides.models import Guide
        from forum.models import ForumPost

        context['featured_destinations'] = Destination.objects.filter(
            is_published=True
        ).order_by('-risk_level', '-updated_at')[:6]

        context['latest_reports'] = TripReport.objects.filter(
            is_approved=True
        ).order_by('-created_at')[:5]

        context['latest_guides'] = Guide.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]

        context['hot_discussions'] = ForumPost.objects.filter(
            is_approved=True
        ).order_by('-reply_count', '-created_at')[:5]

        return context
