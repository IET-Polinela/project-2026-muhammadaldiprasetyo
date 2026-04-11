from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Report

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

# 3. Membuat Laporan Baru (Create)
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

# 4. Mengedit Laporan (Update)
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

# 5. Menghapus Laporan (Delete)
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')

# 6. View Khusus Update Status (Workflow Dasar)
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('report_list')

# 7. Halaman Statis Tentang Saya (Mengarahkan ke app 'about')
class AboutView(TemplateView):
    template_name = 'about/about.html'

# 8. Halaman Statis Kontak (Mengarahkan ke app 'contacts' dan file 'contacts.html')
class ContactView(TemplateView):
    template_name = 'contacts/contacts.html'