from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usermanagement_24782019 import views as user_views 
from main_app.urls import router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782019.api_views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)), 

    # Endpoint Token JWT (Login & Refresh)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', RegisterView.as_view(), name='api_register'),
    
    path('api-auth/', include('rest_framework.urls')),
    
    path('', include('main_app.urls')),
    
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    
    # Login & Logout (Session Base Bawaan / Web View)
    path('login/', auth_views.LoginView.as_view(
        template_name='usermanagement_24782019/login.html',
        redirect_authenticated_user=True 
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', user_views.register_citizen, name='register'),
]
