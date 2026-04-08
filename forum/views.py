from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.utils import timezone
from django.contrib import messages
from .models import ForumCategory, ForumPost, ForumReply
from .forms import ForumPostForm, ForumReplyForm, FeedbackForm


class ForumHomeView(ListView):
    template_name = 'forum/home.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ForumCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = ForumPost.objects.filter(
            is_approved=True
        ).select_related('author', 'category')[:10]
        context['hot_posts'] = ForumPost.objects.filter(
            is_approved=True, is_hot=True
        ).select_related('author', 'category')[:5]
        return context


class ForumCategoryView(ListView):
    template_name = 'forum/category.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(ForumCategory, slug=self.kwargs['slug'])
        return ForumPost.objects.filter(
            category=self.category, is_approved=True
        ).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ForumPostDetailView(DetailView):
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return ForumPost.objects.filter(is_approved=True).select_related('author', 'category')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        ForumPost.objects.filter(pk=self.object.pk).update(view_count=F('view_count') + 1)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.object.replies.filter(
            is_approved=True
        ).select_related('author')
        context['reply_form'] = ForumReplyForm()
        return context


@login_required
def create_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_reply_at = timezone.now()
            post.save()
            messages.success(request, 'Discussion posted.')
            return redirect('forum_post_detail', slug=post.slug)
    else:
        form = ForumPostForm()
    return render(request, 'forum/create_post.html', {'form': form})


@login_required
def add_reply(request, slug):
    post = get_object_or_404(ForumPost, slug=slug, is_approved=True)
    if post.is_locked:
        messages.error(request, 'This discussion is locked.')
        return redirect('forum_post_detail', slug=slug)

    if request.method == 'POST':
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.save()
            post.reply_count = post.replies.filter(is_approved=True).count()
            post.last_reply_at = timezone.now()
            if post.reply_count >= 10:
                post.is_hot = True
            post.save(update_fields=['reply_count', 'last_reply_at', 'is_hot'])
            messages.success(request, 'Reply posted.')
    return redirect('forum_post_detail', slug=slug)

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback! We will review it shortly.')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'forum/feedback.html', {'form': form})