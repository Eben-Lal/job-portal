from django.db import models


class CustomUser(models.Model):
    ROLE_CHOICES = [
        ("JOBSEEKER", "Job Seeker"),
        ("EMPLOYER", "Employer"),
    ]

    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def _str_(self):
        return f"{self.fname} {self.lname} {self.role}"

