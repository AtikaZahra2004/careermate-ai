def calculate_match(user_skills, job_skills):
    user_set = {s.lower() for s in user_skills}
    matched = [s for s in job_skills if s.lower() in user_set]
    missing = [s for s in job_skills if s.lower() not in user_set]
    score = round(len(matched) / len(job_skills) * 100) if job_skills else 0
    return {"score": score, "matched": matched, "missing": missing}