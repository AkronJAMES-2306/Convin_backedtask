from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class User(AbstractUser):
    mobile_validator = RegexValidator(r'^\d{10,15}$')
    mobile_number = models.CharField(max_length=15, validators=[mobile_validator])
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Expense(models.Model):
    SPLIT_METHODS = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]
    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses_created')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='expenses_participating')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True)  
    date = models.DateField()  

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"{self.description} - {self.amount}"
