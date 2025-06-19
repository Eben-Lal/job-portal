from django.db import models
from django.utils import timezone
from api.models import Employer

# Create your models here.


class Job(models.Model):

    JOB_TYPES = (
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    )

    INDUSTRY_CHOICES = [
        ('it', 'Information Technology'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('finance', 'Finance'),
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
    ]
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name='jobs'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPES, default='full-time')
    industry = models.CharField(
        max_length=50, choices=INDUSTRY_CHOICES, default='it')
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"
