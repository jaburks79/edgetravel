from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from .models import TripReport, ReportVote
from .forms import TripReportForm, ReportCommentForm


class ReportListView(ListView):
    template_name = 'reports/list.html'
    context_object_name = 'reports'
    paginate_by = 15

    def get_queryset(self):
        qs = TripReport.objects.filter(is_approved=True).select_related('destination', 'author')
        sort = self.request.GET.get('sort', 'newest')
        dest = self.request.GET.get('destination')
        if dest:
            qs = qs.filter(destination__slug=dest)
        if sort == 'top':
            qs = qs.order_by('-upvotes')
        elif sort == 'featured':
            qs = qs.filter(is_featured=True).order_by('-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        return context


class ReportDetailView(DetailView):
    template_name = 'reports/detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return TripReport.objects.filter(is_approved=True).select_related('destination', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = ReportCommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True)
        if self.request.user.is_authenticated:
            context['user_voted'] = ReportVote.objects.filter(
                user=self.request.user, report=self.object
            ).exists()
        return context


@login_required
def submit_report(request):
    if request.method == 'POST':
        form = TripReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            messages.success(
                request,
                'Your trip report has been submitted and is awaiting review. '
                'It will be published once approved by our team.'
            )
            return redirect('report_list')
    else:
        form = TripReportForm()
    return render(request, 'reports/submit.html', {'form': form})


@login_required
def vote_report(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    report = get_object_or_404(TripReport, slug=slug, is_approved=True)

    # Prevent self-voting
    if report.author == request.user:
        return JsonResponse({'error': 'Cannot vote on your own report'}, status=400)

    vote, created = ReportVote.objects.get_or_create(
        user=request.user, report=report
    )

    if created:
        report.upvotes += 1
        report.save(update_fields=['upvotes'])
        return JsonResponse({'upvotes': report.upvotes, 'voted': True})
    else:
        # Undo vote
        vote.delete()
        report.upvotes = max(0, report.upvotes - 1)
        report.save(update_fields=['upvotes'])
        return JsonResponse({'upvotes': report.upvotes, 'voted': False})


@login_required
def add_comment(request, slug):
    report = get_object_or_404(TripReport, slug=slug, is_approved=True)
    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.report = report
            comment.author = request.user
            comment.save()
            report.comment_count = report.comments.filter(is_approved=True).count()
            report.save(update_fields=['comment_count'])
            messages.success(request, 'Comment added.')
    return redirect('report_detail', slug=slug)
