from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama (Home) -> http://127.0.0.1:8000/
    path('', views.HomeView.as_view(), name='home'),
    
    # Halaman Daftar Laporan -> http://127.0.0.1:8000/reports/
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    
    # Rute Laporan Lainnya
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', views.ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='delete_report'),
    path('status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
    
    # Halaman statis
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]