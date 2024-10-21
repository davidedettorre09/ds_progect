from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        role = validated_token.get('role')

        if not user_id:
            raise exceptions.AuthenticationFailed(_('No user_id in token'), 'user_id_missing')

        # Crea un oggetto utente virtuale
        user = type('User', (), {})()
        user.id = user_id
        user.role = role
        user.is_authenticated = True
        user.is_active = True
        user.is_anonymous = False

        return user
