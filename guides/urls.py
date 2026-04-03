from django.urls import path
from . import views

urlpatterns = [
    path('', views.GuideListView.as_view(), name='guide_list'),
    path('<slug:slug>/', views.GuideDetailView.as_view(), name='guide_detail'),
]
