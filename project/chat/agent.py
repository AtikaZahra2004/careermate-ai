import json
import os

from groq import Groq

from .models import ChatMessage
from .tools import TOOLS, run_tool

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_STEPS = 5
SYSTEM_PROMPT = """You are CareerMate AI, a friendly job search assistant for freshers in India.
Use the tools to search jobs, check resume match, save jobs, update application status and show a summary.
Rules:
- Never invent jobs, ids or numbers. Use tool results only.
- Do not use tables or markdown tables. When jobs are found, write one short sentence only, because the app already shows job cards below your reply.
- When the user mentions a job by title, search for it first to get its id.
- For a cover letter: call get_my_profile and get_job_details, then write a SHORT letter (under 120 words).
- Keep replies short and clear. If the user writes in Hinglish, reply in simple Hinglish.
- If a tool returns an error, explain it simply and suggest the next step."""

def run_agent(user, text):
    history = list(ChatMessage.objects.filter(user=user).order_by("-created_at")[:10])[::-1]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [{"role": m.role, "content": m.text} for m in history]
    messages.append({"role": "user", "content": text})

    ChatMessage.objects.create(user=user, role="user", text=text)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    jobs = []
    reply = "Sorry, I could not finish that. Please try again."

    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=1500,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            reply = msg.content or reply
            break

        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
        )

        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result = run_tool(user, tc.function.name, args)
            if tc.function.name == "search_jobs" and "jobs" in result:
                jobs = result["jobs"]
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result),
                }
            )

    ChatMessage.objects.create(user=user, role="assistant", text=reply)
    return reply, jobs