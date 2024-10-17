from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdmin  # Assicurati che il permesso personalizzato esista
import logging
from .serializers import CustomTokenObtainPairSerializer
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


# Vista per il login
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    

    if user is not None:
        # Genera il token JWT
        refresh = RefreshToken.for_user(user)
        
        # Aggiungi l'ID dell'utente e il ruolo al token JWT
        refresh['user_id'] = user.id
        refresh['role'] = user.role  # Assumendo che tu abbia un campo 'role'
        
        # Restituisci i token JWT (access e refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)