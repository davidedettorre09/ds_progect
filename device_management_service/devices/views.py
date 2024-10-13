from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer
import requests
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

base_api_url_user_dev = os.getenv('BASE_API_URL_USER_DEV')

# URL di base del microservizio User, prendi il valore da una variabile d'ambiente
base_api_url_user_dev = os.getenv('BASE_API_URL_USER_DEV')

def get_user_info(user_id):
    # Chiamata API al microservizio User per ottenere le informazioni sull'utente
    response = requests.get(f'{base_api_url_user_dev}/users/{user_id}/')
    
    if response.status_code == 200:
        return response.json()  # Restituisce i dati dell'utente
    else:
        raise serializers.ValidationError("User not found")

@permission_classes([IsAuthenticated])
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner_id')
        # Verifica che l'utente esista chiamando il microservizio User
        user_info = get_user_info(owner_id)  # Chiama la funzione per ottenere i dati dell'utente
        
        # Se l'utente esiste, salva il dispositivo
        serializer.save(owner_id=owner_id)

class IsAdminOrReadOnly(IsAuthenticated):
    """
    Permesso che permette solo agli admin di eseguire operazioni CRUD, gli altri possono solo leggere.
    """
    def has_permission(self, request, view):
        # Verifica se l'utente è autenticato
        user = request.user
        
        # Solo gli admin possono eseguire operazioni non di lettura
        if request.method in ['POST', 'PUT', 'DELETE']:
            return user.is_authenticated and user.role == 'admin'
        
        # Le operazioni di lettura sono permesse a tutti gli utenti autenticati
        return user.is_authenticated

@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner_id')
        # Verifica che l'utente esista chiamando il microservizio degli utenti
        response = requests.get(f'{base_api_url_user_dev}/users/{owner_id}/')
        if response.status_code == 200:
            serializer.save()
        else:
            raise serializers.ValidationError("L'utente specificato non esiste.")

@permission_classes([IsAuthenticated])
class ClientDeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        # Verifica che l'utente sia autenticato
        user = self.request.user
        if user.role == 'client':
            return Device.objects.filter(owner_id=user.id)
        return Device.objects.none()

@permission_classes([IsAuthenticated])
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_object(self):
        # Ottieni l'oggetto dispositivo
        device = super().get_object()
        user = self.request.user
        
        # Controlla se l'utente è admin
        if user.role == 'admin':
            return device

        # Controlla se l'utente è client e se è il proprietario del dispositivo
        if user.role == 'client' and device.owner_id == user.id:
            return device

        # Se l'utente non è né admin né il proprietario, restituisce un errore
        raise serializers.ValidationError("Non hai il permesso di accedere a questo dispositivo.")

    def update(self, request, *args, **kwargs):
        user = self.request.user
        # Solo gli admin possono aggiornare
        if user.role != 'admin':
            return Response({"detail": "Non hai il permesso di aggiornare questo dispositivo."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        # Solo gli admin possono cancellare
        if user.role != 'admin':
            return Response({"detail": "Non hai il permesso di cancellare questo dispositivo."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
