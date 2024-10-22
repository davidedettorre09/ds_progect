from django.urls import path
from .views import UserListCreateView, UserDetailView, CustomTokenObtainPairView, VerifyTokenView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', VerifyTokenView.as_view(), name='token_verify')
    ]
