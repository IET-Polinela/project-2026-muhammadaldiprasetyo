from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # Ini yang bikin kolomnya muncul di tabel admin
    list_display = ('username', 'email', 'is_admin', 'is_staff') 

admin.site.register(User, UserAdmin)