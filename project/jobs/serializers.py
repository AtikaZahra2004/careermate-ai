from rest_framework import serializers

from applications.models import Application
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    my_status = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id", "title", "company", "city", "description", "skills",
            "min_experience", "max_experience", "job_type", "source",
            "apply_url", "posted_at", "my_status",
        ]

    def get_my_status(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return None
        return (
            Application.objects.filter(user=request.user, job=obj)
            .values_list("status", flat=True)
            .first()
        )