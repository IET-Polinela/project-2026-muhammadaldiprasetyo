from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
# IMPORT FORM KUSTOM KAMU DI SINI
from usermanagement_24782019.forms import CitizenRegistrationForm 
from .models import Report

# --- AUTH VIEWS ---

class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'usermanagement_24782019/login.html' 
    
    def get_success_message(self, cleaned_data):
        role = "Admin" if self.request.user.is_admin else "Citizen"
        return f"Berhasil login sebagai {role}! Selamat datang, {self.request.user.username}."

class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Berhasil logout!")
        return super().dispatch(request, *args, **kwargs)

class RegisterView(SuccessMessageMixin, CreateView):
    # GUNAKAN FORM KUSTOM AGAR TIDAK ERROR 'AttributeError'
    form_class = CitizenRegistrationForm
    template_name = 'usermanagement_24782019/register.html'
    success_url = reverse_lazy('login')
    success_message = "Akun Citizen berhasil dibuat! Silakan login."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = False # Memastikan user baru otomatis menjadi Citizen
        user.save()
        return super().form_valid(form)

# --- CORE VIEWS ---

class HomeView(TemplateView):
    template_name = 'main_app/home.html'

class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

# --- ADMIN CRUD ---

class ReportCreateView(SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')
    success_message = "Laporan baru berhasil ditambahkan!"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang boleh menambah laporan.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

class ReportUpdate_24782019(SuccessMessageMixin, UpdateView):
    model = Report 
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')
    success_message = "Laporan berhasil diperbarui!"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Citizen tidak boleh mengedit.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

class ReportDelete_24782019(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Citizen tidak boleh menghapus.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().form_valid(form)

class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak!")
            return redirect('report_list')
        
        report = get_object_or_404(Report, pk=pk)
        report.status = request.POST.get('status')
        report.save()
        messages.success(request, "Status laporan berhasil diubah!")
        return redirect('report_list')

# --- STATIC ---

class AboutView(TemplateView):
    template_name = 'about/about.html'

class ContactView(TemplateView):
    template_name = 'contacts/contacts.html'