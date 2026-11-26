from flask import Flask, render_template, request, session, jsonify
import mysql.connector
import requests
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "viikko5secret"

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


@app.route("/")
def index():

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id=%s ORDER BY id",
        (session["session_id"],)
    )

    history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", history=history)


@app.route("/chat", methods=["POST"])
def chat():

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    session_id = session["session_id"]

    user_message = request.form["message"]

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (%s,%s,%s)",
        (session_id, "user", user_message)
    )

    conn.commit()

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "tinyllama",
            "prompt": user_message,
            "stream": False
        }
    )

    bot_reply = response.json()["response"]

    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (%s,%s,%s)",
        (session_id, "assistant", bot_reply)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"reply": bot_reply})


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
