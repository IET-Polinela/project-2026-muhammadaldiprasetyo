from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse 
from django.db.models import Count, Q

# IMPORT FORM KUSTOM KAMU DI SINI
from usermanagement_24782019.forms import CitizenRegistrationForm 
from .forms import ReportForm
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

class DashboardView(LoginRequiredMixin, TemplateView):
    """Menampilkan halaman Dashboard Utama"""
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visible_reports = Report.objects.visible_to(self.request.user)
        context['recent_reported'] = visible_reports.order_by('-created_at')[:5]
        return context

@login_required
def dashboard_stats_api(request):
    """Mengembalikan data statistik (JSON) untuk Chart.js"""
    visible_reports = Report.objects.visible_to(request.user)
    status_data = visible_reports.values('status').annotate(total=Count('status'))
    category_data = visible_reports.values('category').annotate(total=Count('category'))
    
    data = {
        'status_labels': [item['status'] for item in status_data],
        'status_values': [item['total'] for item in status_data],
        'category_labels': [item['category'] for item in category_data],
        'category_values': [item['total'] for item in category_data],
    }
    return JsonResponse(data)

@login_required
def report_search_api(request):
    """Fitur Live Search: Mencari data tanpa reload halaman"""
    query = request.GET.get('q', '')
    reports = Report.objects.visible_to(request.user).filter(
        Q(title__icontains=query) | Q(category__icontains=query)
    ).order_by('-updated_at')
    
    results = []
    for r in reports:
        results.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            'status': r.status,
            'location': r.location,
            'can_edit': r.can_edit(request.user),
            'can_delete': r.can_delete(request.user),
            'can_submit': r.can_submit(request.user),
            'can_verify': r.can_verify(request.user),
            'can_update_status': r.can_update_status(request.user),
            'next_status': r.next_workflow_status(),
            'next_status_label': r.next_workflow_label(),
            'next_status_action_label': r.next_workflow_action_label(),
        })
    return JsonResponse({'results': results})

# ==========================================
# 3. CORE VIEWS (HOME, LIST, DETAIL)
# ==========================================

class HomeView(TemplateView):
    template_name = 'main_app/home.html'

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.visible_to(self.request.user).order_by('-updated_at')

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.visible_to(self.request.user)

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

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            messages.error(request, "Admin tidak dapat membuat laporan citizen.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        if self.request.POST.get('action') == 'submit':
            form.instance.status = Report.Status.REPORTED
            messages.success(self.request, "Laporan berhasil diajukan.")
        else:
            form.instance.status = Report.Status.DRAFT
            messages.success(self.request, "Laporan berhasil disimpan sebagai draft.")
        return super().form_valid(form)

class ReportUpdate_24782019(LoginRequiredMixin, UpdateView):
    model = Report 
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        if self.request.user.is_admin:
            return Report.objects.none()
        return Report.objects.filter(
            reporter=self.request.user,
            status=Report.Status.DRAFT,
        )

    def form_valid(self, form):
        if self.request.POST.get('action') == 'submit':
            form.instance.status = Report.Status.REPORTED
            messages.success(self.request, "Draft berhasil diajukan dan kini terkunci.")
        else:
            form.instance.status = Report.Status.DRAFT
            messages.success(self.request, "Perubahan draft berhasil disimpan.")
        return super().form_valid(form)

class ReportDelete_24782019(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        if self.request.user.is_admin:
            return Report.objects.none()
        return Report.objects.filter(
            reporter=self.request.user,
            status=Report.Status.DRAFT,
        )

    def form_valid(self, form):
        messages.success(self.request, "Draft laporan berhasil dihapus.")
        return super().form_valid(form)

class ReportSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(
            Report,
            pk=pk,
            reporter=request.user,
            status=Report.Status.DRAFT,
        )
        if request.user.is_admin:
            messages.error(request, "Admin tidak dapat mengajukan laporan citizen.")
            return redirect('report_list')

        report.status = Report.Status.REPORTED
        report.save(update_fields=['status', 'updated_at'])
        messages.success(request, "Draft berhasil diajukan dan kini terkunci.")
        return redirect('report_list')

class ReportUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "Hanya admin yang dapat memverifikasi laporan.")
            return redirect('report_list')
        
        report = get_object_or_404(
            Report.objects.visible_to(request.user),
            pk=pk,
        )
        next_status = report.next_workflow_status()
        if request.POST.get('status') != next_status:
            messages.error(request, "Status laporan harus maju sesuai urutan workflow.")
            return redirect('report_list')

        report.status = next_status
        report.save(update_fields=['status', 'updated_at'])
        messages.success(request, f"Status laporan berhasil diubah menjadi {report.get_status_display()}.")
        return redirect('report_list')

# ==========================================
# 5. STATIC VIEWS
# ==========================================

class AboutView(TemplateView):
    template_name = 'about/about.html'

class ContactView(TemplateView):
    template_name = 'contacts/contacts.html'
