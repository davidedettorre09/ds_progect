from django.urls import path
from .views import DeviceListCreateView, DeviceDetailView

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
]
