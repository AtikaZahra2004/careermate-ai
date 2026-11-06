import logging
import os

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .agent import run_agent
from .models import ChatMessage

logger = logging.getLogger(__name__)


class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "chat"

    def get(self, request):
        msgs = ChatMessage.objects.filter(user=request.user).order_by("-created_at")[:50]
        data = [
            {"role": m.role, "text": m.text, "created_at": m.created_at}
            for m in reversed(list(msgs))
        ]
        return Response(data)

    def post(self, request):
        text = (request.data.get("message") or "").strip()
        if not text:
            return Response({"error": "Message is required."}, status=400)
        if len(text) > 1000:
            return Response({"error": "Message is too long (max 1000 characters)."}, status=400)
        if not os.getenv("GROQ_API_KEY"):
            return Response({"error": "AI is not configured on the server."}, status=500)

        try:
            reply, jobs = run_agent(request.user, text)
        except Exception:
            logger.exception("Chat agent failed")
            return Response(
                {"error": "AI service is busy right now. Please try again."}, status=503
            )
        return Response({"reply": reply, "jobs": jobs})

    def delete(self, request):
        ChatMessage.objects.filter(user=request.user).delete()
        return Response({"message": "Chat cleared."})