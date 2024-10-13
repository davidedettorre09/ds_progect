from django.urls import path
from .views import UserListCreateView, UserDetailView
from django.urls import path
from .views import login_user  # Assicurati che la vista di login sia importata

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/login/', login_user, name='login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
