from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', views.ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='delete_report'),
    path('status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
    
    # Path untuk halaman statis
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]