from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        # Menghubungkan form dengan model Report yang sudah dibuat di Lab 3 [cite: 130, 131]
        model = Report
        
        # Menentukan field apa saja yang akan ditampilkan di halaman web [cite: 132, 133]
        fields = ['title', 'category', 'description', 'location']
        
        # Opsi tambahan (Opsional): Menambahkan styling class agar tampilan lebih rapi
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Laporan'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kategori (Misal: Jalan Rusak)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokasi Kejadian'}),
        }