from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782019 import views as user_views 
# Import router yang tadi kita buat di main_app
from main_app.urls import router 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. JALUR API LAB 9 (Sesuai Gambar)
    # Ini akan membuat alamat: http://127.0.0.1:8000/api/report/
    path('api/', include(router.urls)), 
    
    # 2. JALUR HOME & WEB (Tanpa Prefix)
    # Ini akan membuat alamat: http://127.0.0.1:8000/ membuka Home kamu
    path('', include('main_app.urls')),
    
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # Login & Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='usermanagement_24782019/login.html',
        redirect_authenticated_user=True 
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', user_views.register_citizen, name='register'),
]