from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URL per l'admin di Django
    path('api/devices/', include('devices.urls')),  # Include le URL del microservizio dei dispositivi
]
