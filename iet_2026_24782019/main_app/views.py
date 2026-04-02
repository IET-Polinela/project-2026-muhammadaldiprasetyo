from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

# 1. READ: Menampilkan semua daftar laporan
def report_list(request):
    reports = Report.objects.all().order_by('-created_at') # Urutkan dari yang terbaru
    return render(request, 'main_app/report_list.html', {'reports': reports})

# 2. CREATE: Menambah laporan baru
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'main_app/add_report.html', {'form': form, 'title': 'Tambah Laporan'})

# 3. UPDATE: Mengubah laporan yang sudah ada
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'main_app/add_report.html', {'form': form, 'title': 'Edit Laporan'})

# 4. DELETE: Menghapus laporan
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        report.delete()
        return redirect('report_list')
    return render(request, 'main_app/delete_confirm.html', {'report': report})