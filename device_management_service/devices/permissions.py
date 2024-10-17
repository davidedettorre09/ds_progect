from rest_framework.permissions import IsAuthenticated


# Custom permission class that allows only admins to perform CRUD operations, while other users can only read.
class IsAdminOrReadOnly(IsAuthenticated):
    """
    Custom permission class that allows only admins to perform CRUD operations, while other users can only read.
    """

    def has_permission(self, request, view):
        # Obtain the user role from request.user
        user_role = request.user.role

        # Only admins can perform POST, PUT, DELETE operations
        if request.method in ['POST', 'PUT', 'DELETE']:
            return user_role == 'admin'

        # The user can perform GET operations
        return True
