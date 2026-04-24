from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama
    path('', views.HomeView.as_view(), name='home'),
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    
    # Fitur Admin
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', views.ReportUpdate_24782019.as_view(), name='update_report'),
    path('delete/<int:pk>/', views.ReportDelete_24782019.as_view(), name='delete_report'),
    path('status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
    
    # Halaman Statis
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Autentikasi
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]