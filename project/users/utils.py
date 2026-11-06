import re
from pypdf import PdfReader

SKILLS = [
    "Python", "Django", "Django REST Framework", "REST API", "Flask", "FastAPI",
    "JavaScript", "TypeScript", "React", "Redux", "Node.js", "Express",
    "HTML", "CSS", "Tailwind", "Bootstrap", "Next.js",
    "MySQL", "PostgreSQL", "SQL", "MongoDB", "Redis", "SQLite",
    "Git", "GitHub", "Docker", "AWS", "Linux", "JWT", "Celery",
    "Testing", "Pytest", "Postman", "Java", "C++", "Machine Learning",
    "Pandas", "NumPy",
]


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


def extract_skills(text):
    found = []
    for skill in SKILLS:
        pattern = r"(?<![A-Za-z0-9+#])" + re.escape(skill) + r"(?![A-Za-z0-9+#])"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)
    return found