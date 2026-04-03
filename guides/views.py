from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import Guide, GuideCategory


class GuideListView(ListView):
    template_name = 'guides/list.html'
    context_object_name = 'guides'
    paginate_by = 12

    def get_queryset(self):
        qs = Guide.objects.filter(is_published=True).select_related('category', 'destination', 'author')
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GuideCategory.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['featured'] = Guide.objects.filter(
            is_published=True, is_featured=True
        ).first()
        return context


class GuideDetailView(DetailView):
    template_name = 'guides/detail.html'
    context_object_name = 'guide'

    def get_queryset(self):
        return Guide.objects.filter(is_published=True).select_related('category', 'destination', 'author')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment read count
        Guide.objects.filter(pk=self.object.pk).update(read_count=F('read_count') + 1)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_guides'] = Guide.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        return context
