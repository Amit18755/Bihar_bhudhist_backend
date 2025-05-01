from django.db import models
from django.contrib.auth.models import User

class ExtendedUser(models.Model):
    ROLE_CHOICES = [
        ('super admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('none', 'None'),
    ]

    username = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='none')
    auth_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  
        db_column='auth_user_id'
    )
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username
