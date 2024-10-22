from django.urls import path
from .views import DeviceListCreateView, ClientDeviceListView, DeviceDetailView

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),  # Lista e creazione dei dispositivi
    path('my-devices/', ClientDeviceListView.as_view(), name='client-device-list'),  # Lista dei dispositivi dell'utente
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),  # Dettaglio, modifica e cancellazione dei dispositivi
]
