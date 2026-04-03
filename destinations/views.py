from django.views.generic import ListView, DetailView


class DestinationListView(ListView):
    template_name = 'destinations/list.html'
    context_object_name = 'destinations'
    paginate_by = 12

    def get_queryset(self):
        from .models import Destination
        qs = Destination.objects.filter(is_published=True)
        region = self.request.GET.get('region')
        risk = self.request.GET.get('risk')
        search = self.request.GET.get('q')
        if region:
            qs = qs.filter(region=region)
        if risk:
            qs = qs.filter(risk_level=int(risk))
        if search:
            qs = qs.filter(name__icontains=search)
        return qs.order_by('-risk_level', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Destination
        context['regions'] = Destination.REGIONS
        context['risk_levels'] = Destination.RISK_LEVELS
        context['current_region'] = self.request.GET.get('region', '')
        context['current_risk'] = self.request.GET.get('risk', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DestinationDetailView(DetailView):
    template_name = 'destinations/detail.html'
    context_object_name = 'destination'

    def get_queryset(self):
        from .models import Destination
        return Destination.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from reports.models import TripReport
        context['trip_reports'] = TripReport.objects.filter(
            destination=self.object, is_approved=True
        ).order_by('-upvotes')[:10]
        return context
