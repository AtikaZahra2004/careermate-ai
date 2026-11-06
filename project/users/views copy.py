from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Resume
from .serializers import RegisterSerializer, ProfileSerializer, ResumeSerializer
from .utils import extract_text_from_pdf, extract_skills


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Registered successfully. Please login."},
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return Response(ProfileSerializer(profile).data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResumeUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()
        if not resume:
            return Response({"message": "No resume uploaded yet."}, status=404)
        return Response(ResumeSerializer(resume).data)

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Please upload a PDF with key 'file'."}, status=400)
        if not file.name.lower().endswith(".pdf"):
            return Response({"error": "Only PDF files are allowed."}, status=400)
        if file.size > 5 * 1024 * 1024:
            return Response({"error": "File is too large (max 5 MB)."}, status=400)

        try:
            text = extract_text_from_pdf(file)
        except Exception:
            return Response({"error": "Could not read this PDF."}, status=400)

        if not text.strip():
            return Response(
                {"error": "No text found. Upload a text-based PDF, not a scanned image."},
                status=400,
            )

        skills = extract_skills(text)
        file.seek(0)
        resume = Resume.objects.create(
            user=request.user, file=file, extracted_text=text, extracted_skills=skills
        )

        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.skills = skills
        profile.save()

        return Response(ResumeSerializer(resume).data, status=201)