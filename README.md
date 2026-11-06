# CareerMate AI

An AI-powered job search assistant for freshers. Chat with the AI to search jobs, check how well your resume matches, and track every application in one place.

**Live demo:** _add link after deploy_

## Features

- Register and login with JWT authentication
- Job search with filters (keyword, city, job type) and pagination
- Resume upload (PDF) with automatic skill detection
- Resume-to-job match score with matched and missing skills
- Application tracker (Saved, Applied, Interview, Offer, Rejected) and dashboard
- Apply button that opens the official careers page and marks the job as applied
- AI chat agent using LLM function calling: search jobs, check match, save jobs, update status, summarize progress
- Rate limiting on the API

## Tech stack

- **Backend:** Python, Django, Django REST Framework, SimpleJWT
- **Frontend:** React (Vite), React Router, Axios
- **Database:** MySQL
- **AI:** Groq API (LLM with tool calling)

## How the AI agent works

The user sends a message. The LLM decides which backend tool to call (for example `search_jobs` or `match_resume`). Django runs the tool for the logged-in user only, and returns the result to the LLM, which writes the final reply. The AI never invents jobs. It only uses database results.

## Screenshots

_add screenshots here: dashboard, jobs, tracker, AI chat_

## Run locally

### Backend

```bash
cd project
python -m venv ../env
../env/Scripts/activate        # Windows
pip install -r requirements.txt
cp .env.example .env           # then fill in your values
python manage.py migrate
python manage.py createsuperuser
python seed_jobs.py
python manage.py runserver
```

Create a MySQL database named `careermate` first.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Main API endpoints

| Method          | Endpoint                     | Purpose                  |
| --------------- | ---------------------------- | ------------------------ |
| POST            | /api/auth/register/          | Create account           |
| POST            | /api/auth/login/             | Get JWT tokens           |
| GET/PUT         | /api/auth/me/                | Profile                  |
| GET/POST        | /api/auth/resume/            | Resume upload and skills |
| GET             | /api/jobs/                   | Search and filter jobs   |
| GET             | /api/jobs/{id}/match/        | Match score              |
| GET/POST        | /api/applications/           | Tracker                  |
| POST            | /api/applications/apply/     | Mark as applied          |
| GET             | /api/applications/dashboard/ | Dashboard counts         |
| GET/POST/DELETE | /api/chat/                   | AI chat                  |

## Author

Atika Zahra
