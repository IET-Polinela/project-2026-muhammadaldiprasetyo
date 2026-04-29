from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse 
from django.db.models import Count 

# IMPORT FORM KUSTOM KAMU DI SINI
from usermanagement_24782019.forms import CitizenRegistrationForm 
from .models import Report

# ==========================================
# 1. AUTH VIEWS (LOGIN, LOGOUT, REGISTER)
# ==========================================

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
    form_class = CitizenRegistrationForm
    template_name = 'usermanagement_24782019/register.html'
    success_url = reverse_lazy('login')
    success_message = "Akun Citizen berhasil dibuat! Silakan login."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_admin = False 
        user.save()
        return super().form_valid(form)

# ==========================================
# 2. LAB 7 VIEWS (DASHBOARD & AJAX API)
# ==========================================

class DashboardView(TemplateView):
    """Menampilkan halaman Dashboard Utama"""
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Menampilkan tabel 5 laporan terakhir (REPORTED) dan 5 selesai (RESOLVED)
        context['recent_reported'] = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
        context['recent_resolved'] = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]
        return context

def dashboard_stats_api(request):
    """Mengembalikan data statistik (JSON) untuk Chart.js"""
    status_data = Report.objects.values('status').annotate(total=Count('status'))
    category_data = Report.objects.values('category').annotate(total=Count('category'))
    
    data = {
        'status_labels': [item['status'] for item in status_data],
        'status_values': [item['total'] for item in status_data],
        'category_labels': [item['category'] for item in category_data],
        'category_values': [item['total'] for item in category_data],
    }
    return JsonResponse(data)

def report_search_api(request):
    """Fitur Live Search: Mencari data tanpa reload halaman"""
    query = request.GET.get('q', '')
    reports = Report.objects.filter(title__icontains=query) | Report.objects.filter(category__icontains=query)
    
    results = []
    for r in reports:
        results.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            'status': r.status,
            'location': r.location,
        })
    return JsonResponse({'results': results})

# ==========================================
# 3. CORE VIEWS (HOME, LIST, DETAIL)
# ==========================================

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

    def render_to_response(self, context, **kwargs):
        # Jika request datang dari AJAX (untuk Modal Detail), kirim JSON
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {
                'title': self.object.title,
                'description': self.object.description,
                'status': self.object.status,
                'category': self.object.category,
                'location': self.object.location,
            }
            return JsonResponse(data)
        return super().render_to_response(context, **kwargs)

# ==========================================
# 4. ADMIN CRUD (CREATE, UPDATE, DELETE)
# ==========================================

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

# ==========================================
# 5. STATIC VIEWS
# ==========================================

class AboutView(TemplateView):
    template_name = 'about/about.html'

class ContactView(TemplateView):
    template_name = 'contacts/contacts.html'