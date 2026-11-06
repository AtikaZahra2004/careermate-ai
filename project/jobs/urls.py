from django.urls import path
from .views import JobListView, JobDetailView, JobMatchView

urlpatterns = [
    path("", JobListView.as_view(), name="job-list"),
    path("<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("<int:pk>/match/", JobMatchView.as_view(), name="job-match"),
]