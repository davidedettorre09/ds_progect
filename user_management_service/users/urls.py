from django.urls import path
from .views import UserListCreateView, UserDetailView, login_user  # Importa le viste necessarie
from .views import CustomTokenObtainPairView
urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    ]
