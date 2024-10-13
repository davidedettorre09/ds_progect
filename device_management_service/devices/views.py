from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .models import Device
from .serializers import DeviceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Permesso personalizzato che permette solo agli admin di eseguire operazioni CRUD
class IsAdminOrReadOnly(IsAuthenticated):
    """
    Permesso che permette solo agli admin di eseguire operazioni CRUD, mentre gli altri utenti possono solo leggere.
    """
    def has_permission(self, request, view):
        # Ottiene il ruolo dell'utente tramite request.user
        user_role = request.user.role

        # Solo gli admin possono eseguire operazioni non di lettura
        if request.method in ['POST', 'PUT', 'DELETE']:
            return user_role == 'admin'
        
        # Le operazioni di lettura sono permesse a tutti gli utenti autenticati
        return True

@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        # Salva il dispositivo associato all'owner_id specificato
        owner_id = self.request.data.get('owner_id')
        if owner_id:
            serializer.save(owner_id=owner_id)
        else:
            raise serializers.ValidationError("Owner ID not provided")

@permission_classes([IsAuthenticated])
class ClientDeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        # Ottiene il ruolo e l'ID dell'utente da request.user
        user_role = self.request.user.role
        user_id = self.request.user.id

        # Se l'utente è un client, restituisce solo i dispositivi associati all'utente
        if user_role == 'client':
            return Device.objects.filter(owner_id=user_id)
        return Device.objects.none()

@permission_classes([IsAuthenticated])
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_object(self):
        device = super().get_object()
        user_role = self.request.user.role
        user_id = self.request.user.id

        # Se l'utente è admin, restituisce il dispositivo
        if user_role == 'admin':
            return device
        
        # Se l'utente è client e proprietario del dispositivo, restituisce il dispositivo
        if user_role == 'client' and device.owner_id == user_id:
            return device

        # Se l'utente non è né admin né proprietario, blocca l'accesso
        raise serializers.ValidationError("Non hai il permesso di accedere a questo dispositivo.")

    def update(self, request, *args, **kwargs):
        user_role = self.request.user.role

        # Solo gli admin possono aggiornare
        if user_role != 'admin':
            return Response({"detail": "Non hai il permesso di aggiornare questo dispositivo."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user_role = self.request.user.role

        # Solo gli admin possono cancellare
        if user_role != 'admin':
            return Response({"detail": "Non hai il permesso di cancellare questo dispositivo."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
