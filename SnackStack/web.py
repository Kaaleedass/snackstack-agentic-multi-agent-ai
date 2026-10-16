"""Flask web interface for the SnackStack LangGraph assistant.

Run from the outer project folder:
    python web.py
"""

import os
import uuid

from flask import Flask, jsonify, render_template, request, session, Response
from langgraph.types import Command, Overwrite

from SnackStack.config import get_logger, openai_client
from SnackStack.graph import graph

logger = get_logger("web")
app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "snackstack-dev-change-this-key"
)


def get_graph_config():
    if "thread_id" not in session:
        session["thread_id"] = str(uuid.uuid4())
    return {"configurable": {"thread_id": session["thread_id"]}}


def get_pending_interrupts(config):
    snapshot = graph.get_state(config)
    return [
        item
        for task in snapshot.tasks
        for item in task.interrupts
    ]


def run_assistant(message: str):
    config = get_graph_config()
    pending = get_pending_interrupts(config)

    if pending:
        result = graph.invoke(Command(resume=message), config=config)
    else:
        result = graph.invoke(
            {
                "user_query": message,
                "agent_results": Overwrite([]),
            },
            config=config,
        )

    pending = get_pending_interrupts(config)
    if pending:
        return {"reply": str(pending[0].value), "needs_input": True}

    answer = result.get("final_answer") if isinstance(result, dict) else None
    if not answer:
        snapshot = graph.get_state(config)
        answer = snapshot.values.get("final_answer") if snapshot.values else None
    if not answer:
        answer = "Sorry, I couldn't generate a response. Please try again."

    return {"reply": str(answer), "needs_input": False}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please type a message first."}), 400

    try:
        logger.info("Incoming web message: %s", message[:160])
        return jsonify(run_assistant(message))
    except Exception:
        logger.exception("Web chat request failed.")
        return jsonify({
            "error": "Something went wrong. Check the web.py terminal for details."
        }), 500


@app.post("/api/speak")
def speak():
    """Generate speech with OpenAI TTS and return a WAV audio response."""
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    voice = str(payload.get("voice", "nova")).strip().lower()
    allowed_voices = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}

    if not text:
        return jsonify({"error": "No text was provided for speech."}), 400
    if voice not in allowed_voices:
        return jsonify({"error": "Unsupported voice selection."}), 400
    if len(text) > 4000:
        text = text[:4000]

    try:
        audio = openai_client.audio.speech.create(
            model="tts-1", voice=voice, input=text, response_format="wav"
        )
        return Response(audio.content, mimetype="audio/wav")
    except Exception:
        logger.exception("OpenAI text-to-speech request failed.")
        return jsonify({"error": "Speech generation failed. Check the web.py terminal and OpenAI API configuration."}), 500


@app.post("/api/reset")
def reset():
    session["thread_id"] = str(uuid.uuid4())
    return jsonify({"reply": "New conversation started."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
