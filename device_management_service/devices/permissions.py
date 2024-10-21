from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        logger.info(f"Request.auth: {request.auth}")  # Log dei dati del token

        if request.method in permissions.SAFE_METHODS:
            return True

        role = request.auth.get('role')
        user_id = request.auth.get('user_id')

        logger.info(f"Role: {role}, User ID: {user_id}, Owner ID: {obj.owner_id}")

        return role == 'admin' or obj.owner_id == user_id
