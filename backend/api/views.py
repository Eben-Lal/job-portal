
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import SignupSerializer
# from .models import CustomUser
from django.conf import settings
# import jwt
# from datetime import datetime, timedelta
from .serializers import CustomUserSerializer
from rest_framework import viewsets, generics
from .models import JobSeeker, Employer
from .serializers import JobSeekerSerializer, EmployerSerializer
from rest_framework import filters
from rest_framework import generics
from jobapp.models import Job
from jobapp.serializers import JobSerializer
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


class Logoutview(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response


class JobSeekerViewSet(viewsets.ModelViewSet):

    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobSearchView(generics.ListAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class ApplyToJobView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        seeker = self.request.user
        job = serializer.validated_data['job']

        #  Prevent duplicate applications
        if Application.objects.filter(job=job, seeker=seeker).exists():
            raise ValidationError("You have already applied to this job.")

        serializer.save(seeker=seeker)


class EmployerApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ Allow only employers to view
        if not hasattr(user, 'employer_profile'):
            raise PermissionDenied("Only employers can view applications.")

        # ✅ Filter applications only for jobs posted by this employer
        return Application.objects.filter(job__employer=user.employer_profile)
