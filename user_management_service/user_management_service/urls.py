"""
URL configuration for user_management_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import VerifyTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Per ottenere il token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Per ottenere un nuovo token di accesso
    path('api/token/verify/', VerifyTokenView.as_view(), name='token_verify'), # Verifica se il token JWT è ancora valido
    path('api/', include('users.urls')),  # Include le rotte definite in `users/urls.py`
]
