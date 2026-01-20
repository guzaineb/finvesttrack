# apps/users/models.py (ONLY THE USER MODEL - KEEP OTHER FILES AS IS)
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # AJOUTEZ CES 4 LIGNES POUR CORRIGER LE PROBLÈME
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='finvesttrack_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='finvesttrack_user_permissions_set',
        blank=True,
    )
    
    class Meta:
        db_table = 'users'