from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, JobSeeker, Employer


@receiver(post_save, sender=CustomUser)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'jobseeker':
            JobSeeker.objects.create(user=instance)
        elif instance.role == 'employer':
            Employer.objects.create(user=instance)
