from django.db.models import Count
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from jobs.models import Job

from .models import Application
from .serializers import ApplicationSerializer, ApplicationUpdateSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = (
            Application.objects.filter(user=self.request.user)
            .select_related("job")
            .order_by("-updated_at")
        )
        status_value = self.request.query_params.get("status")
        if status_value:
            qs = qs.filter(status=status_value)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.validated_data["job"]
        if Application.objects.filter(user=request.user, job=job).exists():
            return Response(
                {"error": "You have already saved or applied to this job."}, status=400
            )
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related("job")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ApplicationUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ApplicationSerializer(instance).data)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Application.objects.filter(user=request.user)
        counts = {key: 0 for key, _ in Application.STATUS_CHOICES}
        for row in qs.values("status").annotate(n=Count("id")):
            counts[row["status"]] = row["n"]

        recent = ApplicationSerializer(
            qs.select_related("job").order_by("-updated_at")[:5], many=True
        ).data
        return Response({"total": qs.count(), "counts": counts, "recent": recent})
class ApplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            job = Job.objects.get(pk=int(request.data.get("job_id")))
        except (Job.DoesNotExist, TypeError, ValueError):
            return Response({"error": "A valid job_id is required."}, status=400)

        existing = Application.objects.filter(user=request.user, job=job).first()
        if existing and existing.status != "saved":
            # already applied or further along: do not move it backwards
            return Response(ApplicationSerializer(existing).data)

        app, _ = Application.objects.update_or_create(
            user=request.user, job=job, defaults={"status": "applied"}
        )
        return Response(ApplicationSerializer(app).data)