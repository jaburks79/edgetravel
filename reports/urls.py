from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('submit/', views.submit_report, name='submit_report'),
    path('<slug:slug>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('<slug:slug>/vote/', views.vote_report, name='vote_report'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
