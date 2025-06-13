from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        # ('STAFF', 'Staff'),
        # ('DRIVER', 'Driver'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.username