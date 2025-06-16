from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("JOBSEEKER", "Job Seeker"),
        ("EMPLOYER", "Employer"),
    ]

    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)  # Required for login
    is_staff = models.BooleanField(default=False)  # Required for admin

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname']

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.role})"
