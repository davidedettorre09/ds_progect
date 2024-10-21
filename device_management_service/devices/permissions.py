from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        logger.info(f"Request.user: {request.user}")  # Log dei dati dell'utente autenticato

        if request.method in permissions.SAFE_METHODS:
            return True

        # Otteniamo il ruolo e l'ID direttamente dall'oggetto utente
        role = getattr(request.user, 'role', None)  # Assicurati che l'utente abbia il campo 'role'
        user_id = getattr(request.user, 'id', None)

        logger.info(f"Role: {role}, User ID: {user_id}, Owner ID: {obj.owner_id}")

        return role == 'admin' or obj.owner_id == user_id
