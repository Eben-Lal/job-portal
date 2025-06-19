from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.conf import settings
from django.apps import apps


class Role(models.TextChoices):
    JOBSEEKER = 'jobseeker', ('Jobseeker')
    EMPLOYER = 'employer', ('Employer')


class CustomUser(AbstractBaseUser, PermissionsMixin):

    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=15, choices=Role.choices)

    is_active = models.BooleanField(default=True)  # Required for login
    is_staff = models.BooleanField(default=False)  # Required for admin

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname']

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.role})"


class JobSeeker(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='jobseeker_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"Jobseeker: {self.user.email}"


class Employer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Employer: {self.user.email} ({self.company_name})"


class Application(models.Model):
    job = models.ForeignKey(
        'jobapp.Job',  # use app_name.ModelName as a string
        on_delete=models.CASCADE,
        related_name='applications'
    )
    seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(default=timezone.now)
    cover_letter = models.TextField(blank=True)

    class Meta:
        unique_together = ('job', 'seeker')  # prevent duplicate applications

    def __str__(self):
        return f"{self.seeker.email} applied to {self.job.title}"
