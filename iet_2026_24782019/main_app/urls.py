from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# Tetap biarkan konfigurasi router di sini tidak apa-apa
router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = [
    # --- KODE LAMA KAMU (HOME DI PALING ATAS) ---
    path('', views.HomeView.as_view(), name='home'), 
    
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # Fitur Dashboard & Search
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/search-reports/', views.report_search_api, name='report_search_api'),

    # Fitur Admin / Petugas
    path('reports/add/', views.ReportCreateView.as_view(), name='add_report'),
    path('reports/update/<int:pk>/', views.ReportUpdate_24782019.as_view(), name='update_report'),
    path('reports/delete/<int:pk>/', views.ReportDelete_24782019.as_view(), name='delete_report'),
    path('reports/update-status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
    
    # Halaman Statis & Autentikasi
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('app-login/', views.MyLoginView.as_view(), name='app_login'),
    path('app-logout/', views.MyLogoutView.as_view(), name='app_logout'),
    path('app-register/', views.RegisterView.as_view(), name='app_register'),
]