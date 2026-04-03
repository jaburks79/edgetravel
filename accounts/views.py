from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib import messages
from .forms import EdgeTravelRegistrationForm, EdgeTravelLoginForm, ProfileEditForm
from .models import User


class EdgeTravelLoginView(LoginView):
    form_class = EdgeTravelLoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        # Track IP on login
        user = form.get_user()
        user.last_ip = self.get_client_ip()
        user.save(update_fields=['last_ip'])
        return super().form_valid(form)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return self.request.META.get('REMOTE_ADDR')


class EdgeTravelLogoutView(LogoutView):
    next_page = '/'


def register(request):
    if request.method == 'POST':
        form = EdgeTravelRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to EdgeTravel! Your account has been created.')
            return redirect('home')
    else:
        form = EdgeTravelRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        from reports.models import TripReport
        from forum.models import ForumPost
        context['user_reports'] = TripReport.objects.filter(
            author=user, is_approved=True
        ).order_by('-created_at')[:10]
        context['user_posts'] = ForumPost.objects.filter(
            author=user, is_approved=True
        ).order_by('-created_at')[:10]
        return context


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
