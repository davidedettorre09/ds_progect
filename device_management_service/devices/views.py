from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Device
from .serializers import DeviceSerializer
from .permissions import IsAdminOrOwner
from rest_framework.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)


# Lista e creazione dei dispositivi
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Log per verificare il token JWT
        logger.info(f"Token JWT in DeviceListCreateView: {self.request.auth}")

        try:
            # Preleva l'owner_id dal token JWT
            owner_id = self.request.auth.get('user_id')
            if owner_id:
                logger.info(f"Owner ID trovato nel token: {owner_id}")
                serializer.save(owner_id=owner_id)
            else:
                logger.error("Owner ID non trovato nel token JWT.")
                raise serializers.ValidationError("Owner ID not found in token.")
        except Exception as e:
            logger.error(e)
            return Response({
                "Error": f"Unexpected Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Vista per i dispositivi di un singolo utente
class ClientDeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Log per verificare il token JWT
        logger.info(f"Token JWT in ClientDeviceListView: {self.request.auth}")

        user_id = self.request.auth.get('user_id')
        if user_id:
            logger.info(f"User ID trovato nel token: {user_id}")
        else:
            logger.error("User ID non trovato nel token JWT.")

        return Device.objects.filter(owner_id=user_id)


# Dettaglio, aggiornamento e cancellazione dei dispositivi
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_object(self):
        device = super().get_object()
        # Log per verificare il token JWT
        logger.info(f"Token JWT in DeviceDetailView: {self.request.auth}")

        user_role = self.request.auth.get('role')
        user_id = self.request.auth.get('user_id')

        logger.info(f"User role: {user_role}, User ID: {user_id}, Device owner ID: {device.owner_id}")

        # Se l'utente è admin o il proprietario del dispositivo, può accedervi
        if user_role == 'admin' or device.owner_id == user_id:
            logger.info("Accesso consentito.")
            return device

        logger.warning("Accesso negato, l'utente non è né admin né il proprietario del dispositivo.")
        raise PermissionDenied("Non hai il permesso di accedere a questo dispositivo.")
