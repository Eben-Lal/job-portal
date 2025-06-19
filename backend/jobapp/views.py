
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer
from .permissions import IsEmployerOwner


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwner]

    def get_queryset(self):
        # All logged-in users can see all jobs
        return Job.objects.all()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'employer_profile'):
            serializer.save(employer=self.request.user.employer_profile)
        else:
            raise PermissionDenied("Only employers can post jobs.")
