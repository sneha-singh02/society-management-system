from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_ADMIN = 'ADMIN'
    ROLE_OWNER = 'OWNER'
    ROLE_TENANT = 'TENANT'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_OWNER, 'Owner'),
        (ROLE_TENANT, 'Tenant'),
    ]

    # reuse built-in is_active field from AbstractUser
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # email should be required
    email = models.EmailField(unique=True)
    # __str__ for readability
    def __str__(self):
        return f"{self.username} ({self.role})"

class Society(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name

class Flat(models.Model):
    flat_number = models.CharField(max_length=50)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'Owner'}
    )

    def __str__(self):
        return f"{self.flat_number} — {self.society.name}"

class MaintenanceBill(models.Model):
    STATUS_CHOICES = (('PAID','Paid'), ('UNPAID','Unpaid'))
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # e.g., 'January 2026'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')

    def __str__(self):
        return f"{self.flat} — {self.month} — {self.status}"
