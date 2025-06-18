from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'employer_profile'):
            serializer.save(employer=self.request.user.employer_profile)
        else:
            raise PermissionDenied("Only employers can post jobs.")
