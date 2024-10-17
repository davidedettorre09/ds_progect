import logging

from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import CustomTokenObtainPairSerializer, UserSerializer

logger = logging.getLogger(__name__)


# Vista per gestire la lista e la creazione degli utenti (solo admin)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Solo gli admin possono gestire utenti


# Vista per gestire un singolo utente (dettagli, aggiornamento e cancellazione) - solo admin
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Solo gli admin possono gestire utenti


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            user = self.get_serializer().user

            # update last login date
            update_last_login(None, user)
            logger.info(f"User {user.username} logged in successfully.")
        else:
            logger.warning(f"Failed login attempt with username: {request.data.get('username')}")

        return response
