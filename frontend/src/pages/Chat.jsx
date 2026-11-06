import { useEffect, useRef, useState } from "react";
import api from "../api/axios";

const SUGGESTIONS = [
  "Bengaluru mein Django ki jobs dikhao",
  "Mera application summary dikhao",
  "Job 1 ke liye mera resume match score batao",
  "Job 1 ke liye short cover letter likho",
];

function Text({ text }) {
  return text.split("\n").map((line, i) => (
    <div key={i} style={{ minHeight: "1.2em" }}>
      {line.split(/(\*\*[^*]+\*\*)/g).map((part, j) =>
        part.startsWith("**") && part.endsWith("**") ? (
          <b key={j}>{part.slice(2, -2)}</b>
        ) : (
          part
        )
      )}
    </div>
  ));
}

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    api
      .get("/chat/")
      .then((res) => setMessages(res.data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const send = async (text) => {
    const message = (text ?? input).trim();
    if (!message || sending) return;
    setError("");
    setInput("");
    setMessages((m) => [...m, { role: "user", text: message }]);
    setSending(true);
    try {
      const { data } = await api.post("/chat/", { message });
      setMessages((m) => [...m, { role: "assistant", text: data.reply, jobs: data.jobs }]);
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong. Please try again.");
    } finally {
      setSending(false);
    }
  };

  const clear = async () => {
    if (!window.confirm("Clear the whole chat?")) return;
    try {
      await api.delete("/chat/");
      setMessages([]);
    } catch {
      setError("Could not clear chat.");
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-head">
        <div>
          <h1 className="page-title">AI Chat</h1>
          <p className="muted">Ask in English or Hinglish. The AI can search, match, save and track jobs.</p>
        </div>
        {messages.length > 0 && (
          <button className="btn-sm" onClick={clear}>Clear chat</button>
        )}
      </div>

      <div className="chat-box">
        {messages.length === 0 && (
          <div>
            <p className="muted">Try one of these:</p>
            <div className="chips">
              {SUGGESTIONS.map((s) => (
                <button key={s} className="chip" onClick={() => send(s)}>{s}</button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role}`}>
            <Text text={m.text} />
            {m.jobs && m.jobs.length > 0 && (
              <div className="chat-jobs">
                {m.jobs.map((j) => (
                  <div className="mini-job" key={j.id}>
                    <b>{j.title}</b>
                    <div className="muted">{j.company} · {j.city} · Job ID {j.id}</div>
                    <div className="skills" style={{ marginTop: 6 }}>
                      {j.skills.map((s) => (
                        <span key={s} className="skill">{s}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {sending && <div className="typing">AI is thinking...</div>}
        <div ref={bottomRef} />
      </div>

      {error && <div className="error">{error}</div>}

      <div className="chat-input">
        <textarea
          rows={1}
          placeholder="Type your message and press Enter"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          aria-label="Message"
        />
        <button className="btn" onClick={() => send()} disabled={sending || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}