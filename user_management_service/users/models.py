from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Crea e salva un utente con nome utente, email e password forniti.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        extra_fields.setdefault('is_active', True)
        user.set_password(password)  # Hashing della password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Crea e salva un superuser con nome utente, email e password forniti.
        """
        extra_fields.setdefault('role', 'admin')  # Assicura che il ruolo del superuser sia admin
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modello utente personalizzato con nome utente e email come identificatori.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('client', 'Client'),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Utilizzato per il pannello di amministrazione

    objects = CustomUserManager()

    # Campo utilizzato come identificatore principale per il login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Restituisce il nome completo dell'utente (puoi modificare per aggiungere altri campi se necessario).
        """
        return self.username

    def get_short_name(self):
        """
        Restituisce il nome breve dell'utente.
        """
        return self.username
