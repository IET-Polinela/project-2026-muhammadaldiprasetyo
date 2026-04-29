from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782019 import views as user_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Semua fitur dashboard, laporan, dan home sudah ada di sini
    path('', include('main_app.urls')),
    
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # BARIS DASHBOARD DI SINI SUDAH DIHAPUS AGAR TIDAK EROR

    # Path Login
    path('login/', auth_views.LoginView.as_view(
        template_name='usermanagement_24782019/login.html'
    ), name='login'),
    
    # Path Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    path('register/', user_views.register_citizen, name='register'),
]