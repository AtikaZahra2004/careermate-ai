import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from jobs.models import Job

JOBS = [
    {
        "title": "Systems Engineer",
        "company": "Infosys",
        "city": "Bengaluru",
        "description": "Entry-level engineering role for fresh graduates. Build, test and support software for client projects, learn through structured training and work in agile teams.",
        "skills": ["Python", "Java", "SQL", "HTML", "CSS", "JavaScript"],
        "min_experience": 0,
        "max_experience": 1,
        "job_type": "Full-time",
        "source": "official careers page",
        "apply_url": "https://www.infosys.com/careers/",
    },
    {
        "title": "Programmer Analyst Trainee (GenC)",
        "company": "Cognizant",
        "city": "Bengaluru",
        "description": "Fresher program for engineering graduates. Join a training period, then work on application development and testing for global clients.",
        "skills": ["Java", "SQL", "React", "JavaScript", "Python"],
        "min_experience": 0,
        "max_experience": 1,
        "job_type": "Full-time",
        "source": "official careers page",
        "apply_url": "https://careers.cognizant.com/global/en",
    },
    {
        "title": "Analyst (Software Engineer)",
        "company": "Capgemini",
        "city": "Bengaluru",
        "description": "Entry-level software role. Write and test code, fix bugs, and work with senior engineers on client delivery projects.",
        "skills": ["Python", "Java", "SQL", "HTML", "CSS"],
        "min_experience": 0,
        "max_experience": 1,
        "job_type": "Full-time",
        "source": "official careers page",
        "apply_url": "https://www.capgemini.com/careers/",
    },
    {
        "title": "System Engineer",
        "company": "Wipro",
        "city": "Bengaluru",
        "description": "Fresher engineering role. Develop and support applications, learn tools and processes through onboarding, and grow into a project engineer.",
        "skills": ["Python", "Java", "SQL", "Git"],
        "min_experience": 0,
        "max_experience": 1,
        "job_type": "Full-time",
        "source": "official careers page",
        "apply_url": "https://careers.wipro.com/",
    },
    {
        "title": "Full Stack Engineer",
        "company": "Urban Vault",
        "city": "Bengaluru",
        "description": "Junior full-stack role building digital products with Python (Django) and React.js. On-site in Bengaluru, for freshers with 0-1 years of experience.",
        "skills": ["Python", "Django", "React", "JavaScript", "REST API"],
        "min_experience": 0,
        "max_experience": 1,
        "job_type": "Full-time",
        "source": "weekday listing",
        "apply_url": "https://www.weekday.works/jobs/python-developer-fresher-jobs-in-bangalore-3",
    },
]

for data in JOBS:
    job, created = Job.objects.update_or_create(
        title=data["title"], company=data["company"], defaults=data
    )
    print(("Created: " if created else "Updated: ") + f"{job.title} at {job.company}")