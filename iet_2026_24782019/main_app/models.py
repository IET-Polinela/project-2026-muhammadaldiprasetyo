from django.db import models

class Report(models.Model):
    # Field untuk judul laporan 
    title = models.CharField(max_length=200) 
    
    # Field untuk kategori (tambahkan max_length=100) 
    category = models.CharField(max_length=100) 
    
    # Field untuk penjelasan detail masalah 
    description = models.TextField() 
    
    # Field untuk lokasi kejadian [cite: 100]
    location = models.CharField(max_length=200) 
    
    # Status laporan dengan nilai default 'REPORTED' [cite: 100, 104]
    status = models.CharField(
        max_length=20, 
        default='REPORTED'
    ) 
    
    # Tanggal pembuatan otomatis saat data disimpan 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title