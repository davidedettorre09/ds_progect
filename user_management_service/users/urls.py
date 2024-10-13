from django.urls import path
from .views import UserListCreateView, UserDetailView, login_user  # Importa le viste necessarie

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/login/', login_user, name='login'),  # Rotta per il login
]
