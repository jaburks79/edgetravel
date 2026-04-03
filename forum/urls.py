from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumHomeView.as_view(), name='forum_home'),
    path('new/', views.create_post, name='forum_create_post'),
    path('c/<slug:slug>/', views.ForumCategoryView.as_view(), name='forum_category'),
    path('<slug:slug>/', views.ForumPostDetailView.as_view(), name='forum_post_detail'),
    path('<slug:slug>/reply/', views.add_reply, name='forum_add_reply'),
]
