from django.shortcuts import render, redirect
from django.contrib import messages # Tambahkan ini
from .forms import CitizenRegistrationForm

def register_citizen(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = False # Citizen otomatis bukan admin
            user.save()
            messages.success(request, "Registrasi berhasil! Silakan login.") # Notifikasi sukses
            return redirect('login')
    else:
        form = CitizenRegistrationForm()
    
    return render(request, 'usermanagement_24782019/register.html', {'form': form})