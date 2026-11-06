from rest_framework import serializers
from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source="job", write_only=True
    )

    class Meta:
        model = Application
        fields = ["id", "job", "job_id", "status", "notes", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "notes"]