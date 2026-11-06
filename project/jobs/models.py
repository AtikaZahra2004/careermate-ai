from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.JSONField(default=list)
    min_experience = models.PositiveIntegerField(default=0)
    max_experience = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=50, default="Full-time")
    source = models.CharField(max_length=100, default="manual")
    posted_at = models.DateTimeField(auto_now_add=True)
    apply_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-posted_at"]

    def __str__(self):
        return f"{self.title} at {self.company}"