from django.urls import path
from .views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    DashboardView,
    ApplyView,
)

urlpatterns = [
    path("", ApplicationListCreateView.as_view(), name="application-list"),
    path("apply/", ApplyView.as_view(), name="application-apply"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("<int:pk>/", ApplicationDetailView.as_view(), name="application-detail"),
]