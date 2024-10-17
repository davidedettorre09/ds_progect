from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .models import Device
from .permissions import IsAdminOrReadOnly
from .serializers import DeviceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        # Save the owner_id if provided in the request data
        owner_id = self.request.data.get('owner_id')
        if owner_id:
            serializer.save(owner_id=owner_id)
        else:
            raise serializers.ValidationError("Owner ID not provided")


@permission_classes([IsAuthenticated])
class ClientDeviceListView(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        # Obtain the user role and user id from request.user
        user_role = self.request.user.role
        user_id = self.request.user.id

        # If the user is a client, return the devices owned by the user
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

        # If the user is an admin, return the device
        if user_role == 'admin':
            return device

        # If the user is a client, return the device only if the user is the owner
        if user_role == 'client' and device.owner_id == user_id:
            return device

        # If the user is not a client and not the owner, raise a permission error
        raise serializers.ValidationError("Non hai il permesso di accedere a questo dispositivo.")

    def update(self, request, *args, **kwargs):
        user_role = self.request.user.role

        # Only admins can update
        if user_role != 'admin':
            return Response({"detail": "Non hai il permesso di aggiornare questo dispositivo."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user_role = self.request.user.role

        # Only admins can delete
        if user_role != 'admin':
            return Response({"detail": "Non hai il permesso di cancellare questo dispositivo."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
