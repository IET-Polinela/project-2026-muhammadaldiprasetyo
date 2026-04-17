from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages # <--- Import ini untuk pesan (Point 8)
from django.contrib.messages.views import SuccessMessageMixin # <--- Import ini untuk pesan (Point 8)
from .models import Report

# --- Halaman Beranda (Home) ---
class HomeView(TemplateView):
    template_name = 'main_app/home.html' # Pastikan path ini sesuai letak home.html kamu

# 1. Menampilkan Daftar Laporan (Read All)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

# 2. Menampilkan Detail Laporan (Read Single)
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

# 3. Membuat Laporan Baru (Create) - Ditambah Alert
class ReportCreateView(SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')
    success_message = "Laporan baru berhasil ditambahkan!" # <--- Pesan Alert

# 4. Mengedit Laporan (Update) - Ditambah Alert
class ReportUpdateView(SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')
    success_message = "Laporan berhasil diperbarui!" # <--- Pesan Alert

# 5. Menghapus Laporan (Delete) - Ditambah Alert
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')
    
    # Khusus DeleteView, kirim pesannya saat fungsi hapus divalidasi
    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil dihapus!") # <--- Pesan Alert
        return super().form_valid(form)

# 6. View Khusus Update Status (Workflow Dasar) - Ditambah Alert
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        
        # Kirim pesan saat status berhasil diubah
        messages.success(request, f"Status laporan berhasil diubah!") # <--- Pesan Alert
        return redirect('report_list')

# 7. Halaman Statis Tentang Saya
class AboutView(TemplateView):
    template_name = 'about/about.html'

# 8. Halaman Statis Kontak
class ContactView(TemplateView):
    template_name = 'contacts/contacts.html'