import logging

from django.contrib.auth.models import update_last_login
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response

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
            # L'utente è nel contesto del serializer dopo la validazione
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # Validare i dati del serializer
            user = serializer.user  # Ora puoi ottenere l'utente validato

            # update last login date
            update_last_login(None, user)
            logger.info(f"User {user.username} logged in successfully.")
        else:
            logger.warning(f"Failed login attempt with username: {request.data.get('username')}")

        return response


class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        try:
            # Verifica se il token è valido
            UntypedToken(token)
            return Response({'valid': True}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError):
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)
