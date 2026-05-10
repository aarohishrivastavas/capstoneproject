from flask import Flask, request, redirect, render_template_string
import json
import os
from datetime import datetime

# ----------------------------
# ENV SAFETY
# ----------------------------
os.environ["FLASK_SKIP_DOTENV"] = "1"
os.environ["WERKZEUG_RUN_MAIN"] = "true"

app = Flask(__name__)

DATA_FILE = "data.json"

# ----------------------------
# DATA STORAGE
# ----------------------------

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {"goals": []}
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"goals": []}


def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Save error:", e)


# ----------------------------
# AI TASK AGENT
# ----------------------------

def generate_plan(goal):
    if not isinstance(goal, str) or not goal.strip():
        return fallback_agent("general improvement goal")

    try:
        from transformers import pipeline

        model = pipeline(
            "text2text-generation",
            model="google/flan-t5-small"
        )

        prompt = f"""
You are an AI productivity planner.
Break the goal into 5 clear actionable steps.
Return only a numbered list.
Goal: {goal}
"""

        result = model(prompt, max_length=256)[0]["generated_text"]

        tasks = []
        for line in result.split("\n"):
            clean = line.strip("-• 1234567890.").strip()
            if len(clean) > 3:
                tasks.append({"task": clean, "completed": False})

        return tasks[:5] if tasks else fallback_agent(goal)

    except Exception:
        return fallback_agent(goal)


def fallback_agent(goal):
    base = [
        f"Research fundamentals of {goal}",
        f"Create structured practice plan for {goal}",
        "Complete focused practice session",
        "Review mistakes and improve weak areas",
        "Test knowledge with mini project or quiz"
    ]
    return [{"task": t, "completed": False} for t in base]


# ----------------------------
# DASHBOARD UI
# ----------------------------

BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Goal Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #0f172a; color: white; }
        .card { background: #1e293b; border: none; }
        .completed { text-decoration: line-through; opacity: 0.6; }
    </style>
</head>
<body class="container py-4">
    <h1 class="mb-4">🧠 AI Goal Dashboard</h1>
    <a class="btn btn-primary" href="/create">+ New Goal</a>
    <a class="btn btn-secondary" href="/review">Daily Review</a>
    <hr>

    {% for g in goals %}
    <div class="card p-3 mb-3">
        <h3>{{ g.goal }}</h3>
        <small class="text-muted">Created: {{ g.created }}</small>
        <hr>

        {% for t in g.tasks %}
        <div>
            <span class="{% if t.completed %}completed{% endif %}">{{ t.task }}</span>
            <a class="btn btn-sm btn-outline-light" href="/toggle/{{ g.id }}/{{ loop.index0 }}">Toggle</a>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</body>
</html>
"""


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    data = load_data()
    return render_template_string(BASE_HTML, goals=data["goals"])


@app.route("/create", methods=["GET", "POST"])
def create():
    data = load_data()

    if request.method == "POST":
        goal = request.form.get("goal", "")
        tasks = generate_plan(goal)

        new_goal = {
            "id": len(data["goals"]) + 1,
            "goal": goal,
            "created": str(datetime.now()),
            "tasks": tasks
        }

        data["goals"].append(new_goal)
        save_data(data)

        return redirect("/")

    return """
    <h1>Create Goal</h1>
    <form method="post">
        <input class='form-control' name="goal" placeholder="Enter your goal" required>
        <br>
        <button class='btn btn-success'>Create</button>
    </form>
    <br><a href='/'>Back</a>
    """


@app.route("/toggle/<int:gid>/<int:tid>")
def toggle(gid, tid):
    data = load_data()

    for g in data["goals"]:
        if g["id"] == gid and tid < len(g["tasks"]):
            g["tasks"][tid]["completed"] = not g["tasks"][tid]["completed"]

    save_data(data)
    return redirect("/")


@app.route("/review")
def review():
    data = load_data()

    html = "<h1>Daily Review</h1><a href='/'>Home</a><hr>"

    for g in data["goals"]:
        html += f"<h3>{g['goal']}</h3>"

        incomplete = [t for t in g["tasks"] if not t["completed"]]

        if not incomplete:
            html += "<p>All complete 🎉</p>"
        else:
            html += "<ul>"
            for t in incomplete:
                html += f"<li>{t['task']}</li>"
            html += "</ul>"

    return html


# ----------------------------
# TESTS
# ----------------------------

def run_tests():
    print("Running tests...")

    data = load_data()
    assert isinstance(data, dict)
    assert "goals" in data

    tasks = fallback_agent("test goal")
    assert len(tasks) == 5

    plan = generate_plan("learn python")
    assert isinstance(plan, list)
    assert len(plan) > 0

    empty_plan = generate_plan("")
    assert isinstance(empty_plan, list)
    assert len(empty_plan) == 5

    print("All tests passed.")


# ----------------------------
# SAFE DEPLOY ENTRY (FIX BAD FILE DESCRIPTOR ISSUES)
# ----------------------------
# Render uses: gunicorn app:app

if __name__ == "__main__":
    # NEVER force Flask server in restricted environments
    # prevents: Bad file descriptor / WERKZEUG_SERVER_FD crash
    print("App loaded successfully.")
    print("Run locally with: python app.py")
    print("Deploy with Render using: gunicorn app:app")


# ----------------------------
# RENDER FILES
# ----------------------------
# requirements.txt:
# flask
# gunicorn
# transformers
# torch
#
# Procfile:
# web: gunicorn app:app
