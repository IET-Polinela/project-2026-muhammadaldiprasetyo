from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count, Q
from django.shortcuts import render

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ambil 5 data terbaru untuk tabel di dashboard
        context['recent_reported'] = Report.objects.all().order_by('-created_at')[:5]
        return context

def dashboard_data(request):
    # Agregasi data untuk Chart.js
    status_data = Report.objects.values('status').annotate(total=Count('status'))
    category_data = Report.objects.values('category').annotate(total=Count('category'))
    
    data = {
        'status_labels': [item['status'] for item in status_data],
        'status_values': [item['total'] for item in status_data],
        'category_labels': [item['category'] for item in category_data],
        'category_values': [item['total'] for item in category_data],
    }
    return JsonResponse(data)

# Halaman khusus Reports (Live Search)
def report_list_view(request):
    return render(request, 'main_app/reports.html')

# API untuk Live Search AJAX
def search_reports_api(request):
    query = request.GET.get('q', '')
    # Filter berdasarkan judul atau kategori
    reports = Report.objects.filter(
        Q(title__icontains=query) | Q(category__icontains=query)
    ).order_by('-created_at')

    results = []
    for r in reports:
        results.append({
            'title': r.title,
            'category': r.category,
            'status': r.status,
            'location': r.location,
        })
    return JsonResponse({'reports': results})