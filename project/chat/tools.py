from django.db.models import Q

from applications.models import Application
from jobs.matching import calculate_match
from jobs.models import Job
from users.models import Profile, Resume

VALID_STATUS = [key for key, _ in Application.STATUS_CHOICES]


def _job_dict(job):
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "city": job.city,
        "skills": job.skills,
        "job_type": job.job_type,
        "experience": f"{job.min_experience}-{job.max_experience} yrs",
    }


def _get_job(job_id):
    try:
        return Job.objects.get(pk=int(job_id))
    except (Job.DoesNotExist, ValueError, TypeError):
        return None


def _user_skills(user):
    resume = Resume.objects.filter(user=user).order_by("-uploaded_at").first()
    if resume and resume.extracted_skills:
        return resume.extracted_skills
    profile = Profile.objects.filter(user=user).first()
    return profile.skills if profile else []


# ---------- Tools ----------

def search_jobs(user, query="", city="", skill="", job_type=""):
    qs = Job.objects.all()
    if query:
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(company__icontains=query)
            | Q(description__icontains=query)
        )
    if city:
        qs = qs.filter(city__iexact=city)
    if job_type:
        qs = qs.filter(job_type__iexact=job_type)

    jobs = list(qs)
    if skill:
        jobs = [j for j in jobs if skill.lower() in [s.lower() for s in j.skills]]

    jobs = [_job_dict(j) for j in jobs[:5]]
    return {"count": len(jobs), "jobs": jobs}


def get_job_details(user, job_id):
    job = _get_job(job_id)
    if not job:
        return {"error": "Job not found."}
    data = _job_dict(job)
    data["description"] = job.description
    return data


def get_my_profile(user):
    profile = Profile.objects.filter(user=user).first()
    return {
        "name": user.first_name or user.username,
        "city": profile.city if profile else "",
        "experience_years": profile.experience_years if profile else 0,
        "skills": _user_skills(user),
    }


def match_resume(user, job_id):
    job = _get_job(job_id)
    if not job:
        return {"error": "Job not found."}
    skills = _user_skills(user)
    if not skills:
        return {"error": "No resume found. Ask the user to upload a resume first."}
    result = calculate_match(skills, job.skills)
    result["job_title"] = job.title
    return result


def save_job(user, job_id):
    job = _get_job(job_id)
    if not job:
        return {"error": "Job not found."}
    _, created = Application.objects.get_or_create(
        user=user, job=job, defaults={"status": "saved"}
    )
    return {"message": "Job saved." if created else "Job was already saved.", "job_title": job.title}


def update_status(user, job_id, status):
    status = (status or "").lower()
    if status not in VALID_STATUS:
        return {"error": f"Status must be one of {VALID_STATUS}."}
    job = _get_job(job_id)
    if not job:
        return {"error": "Job not found."}
    Application.objects.update_or_create(
        user=user, job=job, defaults={"status": status}
    )
    return {"message": f"Status set to {status}.", "job_title": job.title}


def get_summary(user):
    apps = Application.objects.filter(user=user).select_related("job")
    counts = {key: 0 for key in VALID_STATUS}
    for a in apps:
        counts[a.status] += 1
    recent = [
        {"job": a.job.title, "company": a.job.company, "status": a.status}
        for a in apps.order_by("-updated_at")[:5]
    ]
    return {"total": apps.count(), "counts": counts, "recent": recent}


FUNCTIONS = {
    "search_jobs": search_jobs,
    "get_job_details": get_job_details,
    "get_my_profile": get_my_profile,
    "match_resume": match_resume,
    "save_job": save_job,
    "update_status": update_status,
    "get_summary": get_summary,
}


def run_tool(user, name, args):
    func = FUNCTIONS.get(name)
    if not func:
        return {"error": f"Unknown tool: {name}"}
    try:
        return func(user, **args)
    except TypeError:
        return {"error": "Invalid arguments for this tool."}
    except Exception as exc:
        return {"error": str(exc)}


# ---------- Tool descriptions shown to the AI ----------

def _tool(name, description, props=None, required=None):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": props or {},
                "required": required or [],
            },
        },
    }


_JOB_ID = {"job_id": {"type": "integer", "description": "The job id"}}

TOOLS = [
    _tool(
        "search_jobs",
        "Search jobs. Use short keywords. All arguments are optional.",
        {
            "query": {"type": "string", "description": "Keyword like 'django' or 'react'"},
            "city": {"type": "string", "description": "City name like 'Bengaluru'"},
            "skill": {"type": "string", "description": "One skill like 'Python'"},
            "job_type": {"type": "string", "description": "'Full-time' or 'Internship'"},
        },
    ),
    _tool("get_job_details", "Get full details of one job.", _JOB_ID, ["job_id"]),
    _tool("get_my_profile", "Get the user's name, city, experience and skills."),
    _tool(
        "match_resume",
        "Compare the user's resume skills with a job. Returns score, matched and missing skills.",
        _JOB_ID,
        ["job_id"],
    ),
    _tool("save_job", "Save a job to the user's tracker.", _JOB_ID, ["job_id"]),
    _tool(
        "update_status",
        "Change application status of a job: saved, applied, interview, offer or rejected.",
        {**_JOB_ID, "status": {"type": "string"}},
        ["job_id", "status"],
    ),
    _tool("get_summary", "Get the user's application counts and recent applications."),
]