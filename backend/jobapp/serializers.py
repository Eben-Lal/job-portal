from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'location',
            'salary', 'created_at', 'deadline'
        ]
        read_only_fields = ['employer', 'created_at']
