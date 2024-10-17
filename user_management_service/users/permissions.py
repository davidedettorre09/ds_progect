from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permesso che permette solo agli utenti con ruolo 'admin' di accedere.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsClient(BasePermission):
    """
    Permesso che permette agli utenti con ruolo 'client' di accedere alle operazioni di lettura.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'
