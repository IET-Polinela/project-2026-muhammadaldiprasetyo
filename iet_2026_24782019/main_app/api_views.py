from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Agar bisa diakses tanpa login saat praktikum [cite: 93]
    permission_classes = [permissions.AllowAny]
    
    # Ambil semua data laporan dari database [cite: 93]
    queryset = Report.objects.all()
    
    # Gunakan serializer yang sudah kita buat sebelumnya [cite: 94]
    serializer_class = ReportSerializer