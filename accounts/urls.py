from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.EdgeTravelLoginView.as_view(), name='login'),
    path('logout/', views.EdgeTravelLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
