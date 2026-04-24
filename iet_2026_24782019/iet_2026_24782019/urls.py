from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# Import views dari app usermanagement kamu
from usermanagement_24782019 import views as user_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # Path Login
    path('login/', auth_views.LoginView.as_view(
        template_name='usermanagement_24782019/login.html'
    ), name='login'),
    
    # Path Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # TAMBAHKAN BARIS INI: Agar error NoReverseMatch hilang
    path('register/', user_views.register_citizen, name='register'),
]
# iet_2026_24782019/urls.py
path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),