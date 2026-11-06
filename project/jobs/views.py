from django.db.models import Q
from rest_framework import generics, permissions

from .models import Job
from .serializers import JobSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from users.models import Resume, Profile
from .matching import calculate_match

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Job.objects.all()
        p = self.request.query_params

        q = p.get("q")
        city = p.get("city")
        skill = p.get("skill")
        job_type = p.get("job_type")
        exp = p.get("experience")

        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(company__icontains=q)
                | Q(description__icontains=q)
            )
        if city:
            qs = qs.filter(city__iexact=city)
        if job_type:
            qs = qs.filter(job_type__iexact=job_type)
        if skill:
            qs = qs.filter(skills__contains=skill)
        if exp and exp.isdigit():
            qs = qs.filter(min_experience__lte=int(exp), max_experience__gte=int(exp))

        return qs


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

class JobMatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()
        if resume:
            user_skills = resume.extracted_skills
        else:
            profile = Profile.objects.filter(user=request.user).first()
            user_skills = profile.skills if profile else []

        if not user_skills:
            return Response({"error": "Please upload your resume first."}, status=400)

        result = calculate_match(user_skills, job.skills)
        result["job_id"] = job.id
        result["job_title"] = job.title
        return Response(result)    