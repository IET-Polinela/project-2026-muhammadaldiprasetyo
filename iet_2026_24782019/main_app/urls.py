from django.urls import path
from . import views

urlpatterns = [
    # Halaman utama: Daftar Laporan
    path('', views.report_list, name='report_list'),
    
    # Tambah Laporan
    path('add/', views.add_report, name='add_report'),
    
    # Edit Laporan (membutuhkan ID/Primary Key)
    path('update/<int:pk>/', views.update_report, name='update_report'),
    
    # Hapus Laporan (membutuhkan ID/Primary Key)
    path('delete/<int:pk>/', views.delete_report, name='delete_report'),
]