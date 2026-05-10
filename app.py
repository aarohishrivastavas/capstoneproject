"""
AI Goal Dashboard — Professional Edition
Deploy on Render with: gunicorn app:app

requirements.txt:
    flask
    gunicorn

Procfile:
    web: gunicorn app:app
"""

from flask import Flask, request, redirect, render_template_string, jsonify
import json
import os
from datetime import datetime, date

os.environ["FLASK_SKIP_DOTENV"] = "1"

app = Flask(__name__)
DATA_FILE = "data.json"

# ─────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────

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


def next_id(goals):
    return max((g["id"] for g in goals), default=0) + 1


# ─────────────────────────────────────────
# PLANNER AGENT
# ─────────────────────────────────────────

TASK_TEMPLATES = {
    "python": [
        {"task": "Learn core syntax: variables, loops, functions", "frequency": "daily",   "difficulty": "easy",   "priority": "high"},
        {"task": "Complete 2 coding exercises on a practice platform",  "frequency": "daily",   "difficulty": "medium", "priority": "high"},
        {"task": "Build a small project applying what you've learned",  "frequency": "weekly",  "difficulty": "hard",   "priority": "high"},
        {"task": "Read one chapter of Python documentation",            "frequency": "daily",   "difficulty": "easy",   "priority": "medium"},
        {"task": "Review and refactor yesterday's code",                "frequency": "daily",   "difficulty": "medium", "priority": "medium"},
        {"task": "Share or publish a project for feedback",             "frequency": "once",    "difficulty": "hard",   "priority": "low"},
    ],
    "fitness": [
        {"task": "Complete planned workout session",                    "frequency": "daily",   "difficulty": "hard",   "priority": "high"},
        {"task": "Hit daily protein and calorie targets",               "frequency": "daily",   "difficulty": "medium", "priority": "high"},
        {"task": "Log workout metrics (reps, weight, time)",            "frequency": "daily",   "difficulty": "easy",   "priority": "high"},
        {"task": "30-minute active recovery or stretching",             "frequency": "weekly",  "difficulty": "easy",   "priority": "medium"},
        {"task": "Review weekly progress and adjust plan",              "frequency": "weekly",  "difficulty": "medium", "priority": "medium"},
        {"task": "Take progress photos for comparison",                 "frequency": "weekly",  "difficulty": "easy",   "priority": "low"},
    ],
    "study": [
        {"task": "Study core material for 45 focused minutes",         "frequency": "daily",   "difficulty": "hard",   "priority": "high"},
        {"task": "Review and annotate notes from previous session",     "frequency": "daily",   "difficulty": "medium", "priority": "high"},
        {"task": "Complete one practice test or problem set",           "frequency": "weekly",  "difficulty": "hard",   "priority": "high"},
        {"task": "Create flashcards for key concepts",                  "frequency": "daily",   "difficulty": "easy",   "priority": "medium"},
        {"task": "Identify and target weakest topic areas",             "frequency": "weekly",  "difficulty": "medium", "priority": "medium"},
        {"task": "Summarize the week's learning in writing",            "frequency": "weekly",  "difficulty": "medium", "priority": "low"},
    ],
    "language": [
        {"task": "Complete daily language lesson (app or textbook)",    "frequency": "daily",   "difficulty": "medium", "priority": "high"},
        {"task": "Practice speaking or shadowing for 15 minutes",       "frequency": "daily",   "difficulty": "hard",   "priority": "high"},
        {"task": "Review vocabulary flashcards",                        "frequency": "daily",   "difficulty": "easy",   "priority": "high"},
        {"task": "Watch or listen to native content for 20 minutes",   "frequency": "daily",   "difficulty": "easy",   "priority": "medium"},
        {"task": "Write a short paragraph in the target language",      "frequency": "weekly",  "difficulty": "medium", "priority": "medium"},
        {"task": "Have a conversation session or language exchange",    "frequency": "weekly",  "difficulty": "hard",   "priority": "medium"},
    ],
}

KEYWORD_MAP = {
    "python":   ["python", "coding", "programming", "developer", "code", "software"],
    "fitness":  ["gym", "fitness", "workout", "weight", "run", "muscle", "health", "exercise"],
    "study":    ["study", "school", "exam", "test", "gmat", "sat", "gre", "grade", "academic"],
    "language": ["language", "spanish", "french", "japanese", "mandarin", "german", "korean"],
}


def detect_category(goal: str) -> str:
    goal_lower = goal.lower()
    for category, keywords in KEYWORD_MAP.items():
        if any(k in goal_lower for k in keywords):
            return category
    return "general"


def generate_plan(goal: str, timeframe: str = "") -> list:
    if not isinstance(goal, str) or not goal.strip():
        return _generic_tasks("your goal")

    category = detect_category(goal)

    if category in TASK_TEMPLATES:
        tasks = [dict(t) for t in TASK_TEMPLATES[category]]
    else:
        tasks = _generic_tasks(goal)

    for t in tasks:
        t["completed"] = False
        t["note"] = ""

    return tasks


def _generic_tasks(goal: str) -> list:
    return [
        {"task": f"Research and define a clear action plan for: {goal}", "frequency": "once",   "difficulty": "easy",   "priority": "high"},
        {"task": f"Complete one focused session toward {goal}",          "frequency": "daily",  "difficulty": "medium", "priority": "high"},
        {"task": "Track progress and record results",                    "frequency": "daily",  "difficulty": "easy",   "priority": "high"},
        {"task": "Identify and address the biggest current obstacle",    "frequency": "weekly", "difficulty": "hard",   "priority": "medium"},
        {"task": "Review the week and adjust your strategy",             "frequency": "weekly", "difficulty": "medium", "priority": "medium"},
        {"task": "Reach a measurable milestone and document it",         "frequency": "once",   "difficulty": "hard",   "priority": "low"},
    ]


def daily_feedback(goal_obj: dict) -> dict:
    tasks = goal_obj.get("tasks", [])
    total = len(tasks)
    done  = sum(1 for t in tasks if t.get("completed"))
    pct   = round((done / total) * 100) if total else 0

    incomplete = [t["task"] for t in tasks if not t.get("completed")]
    high_prio  = [t["task"] for t in tasks if not t.get("completed") and t.get("priority") == "high"]

    if pct == 100:
        message = "Outstanding — every task is complete. Consider raising the bar or adding stretch goals."
        status  = "success"
    elif pct >= 60:
        message = f"Solid progress at {pct}%. Focus next on: {high_prio[0] if high_prio else incomplete[0]}."
        status  = "good"
    elif pct >= 30:
        message = f"You're at {pct}% — momentum is building. Prioritize: {high_prio[0] if high_prio else incomplete[0]}."
        status  = "warn"
    else:
        message = f"Only {pct}% done. Start small — complete just one high-priority task today."
        status  = "danger"

    return {"message": message, "status": status, "pct": pct, "done": done, "total": total}


# ─────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────

BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GoalFlow — {% block title %}Dashboard{% endblock %}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0a0f1e;
    --surface:   #111827;
    --surface2:  #1a2234;
    --border:    #1e2d45;
    --accent:    #3b82f6;
    --accent2:   #6366f1;
    --success:   #10b981;
    --warn:      #f59e0b;
    --danger:    #ef4444;
    --text:      #f1f5f9;
    --muted:     #64748b;
    --muted2:    #94a3b8;
    --radius:    10px;
    --font:      'DM Sans', sans-serif;
    --mono:      'DM Mono', monospace;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 15px;
    line-height: 1.6;
    min-height: 100vh;
  }

  /* ── NAV ── */
  nav {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .nav-brand {
    font-size: 17px;
    font-weight: 600;
    letter-spacing: -0.3px;
    color: var(--text);
    text-decoration: none;
  }
  .nav-brand span { color: var(--accent); }
  .nav-links { display: flex; gap: 6px; }
  .nav-links a {
    color: var(--muted2);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 6px;
    transition: background 0.15s, color 0.15s;
  }
  .nav-links a:hover { background: var(--surface2); color: var(--text); }

  /* ── LAYOUT ── */
  .page { max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem; }

  /* ── CARDS ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.25rem;
  }
  .card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 1rem;
    gap: 1rem;
  }
  .card-title { font-size: 17px; font-weight: 600; }
  .card-meta  { font-size: 12px; color: var(--muted); margin-top: 3px; font-family: var(--mono); }

  /* ── PROGRESS BAR ── */
  .progress-wrap { margin: 0.75rem 0; }
  .progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--muted2);
    margin-bottom: 5px;
  }
  .progress-bar-bg {
    background: var(--border);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.4s ease;
  }

  /* ── TASK ROW ── */
  .task-list { display: flex; flex-direction: column; gap: 6px; margin-top: 1rem; }
  .task-row {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    transition: border-color 0.15s;
  }
  .task-row:hover { border-color: #2a3f5f; }
  .task-row.done .task-text { text-decoration: line-through; color: var(--muted); }

  .check-btn {
    width: 20px; height: 20px; min-width: 20px;
    border-radius: 5px;
    border: 1.5px solid var(--muted);
    background: transparent;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.15s, border-color 0.15s;
    color: transparent;
    font-size: 12px;
  }
  .task-row.done .check-btn {
    background: var(--success);
    border-color: var(--success);
    color: #fff;
  }

  .task-text { flex: 1; font-size: 14px; }

  /* ── BADGES ── */
  .badges { display: flex; gap: 5px; flex-wrap: wrap; }
  .badge {
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 99px;
    font-family: var(--mono);
  }
  .badge-high     { background: #3b1a1a; color: #fca5a5; border: 1px solid #7f1d1d; }
  .badge-medium   { background: #2d2007; color: #fcd34d; border: 1px solid #78350f; }
  .badge-low      { background: #0d2a1a; color: #6ee7b7; border: 1px solid #065f46; }
  .badge-daily    { background: #1a1f3a; color: #93c5fd; border: 1px solid #1e3a6e; }
  .badge-weekly   { background: #1f1a3a; color: #c4b5fd; border: 1px solid #3b0764; }
  .badge-once     { background: #1a2020; color: #67e8f9; border: 1px solid #155e75; }
  .badge-easy     { background: #0d2a1a; color: #86efac; border: 1px solid #14532d; }
  .badge-hard     { background: #3b1a1a; color: #fca5a5; border: 1px solid #7f1d1d; }

  /* ── FEEDBACK BANNER ── */
  .feedback-banner {
    border-radius: var(--radius);
    padding: 12px 16px;
    font-size: 14px;
    margin-bottom: 1.25rem;
    border: 1px solid;
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }
  .feedback-success { background: #052e16; border-color: #14532d; color: #bbf7d0; }
  .feedback-good    { background: #0f172a; border-color: #1e3a6e; color: #bfdbfe; }
  .feedback-warn    { background: #1c1007; border-color: #78350f; color: #fde68a; }
  .feedback-danger  { background: #1a0505; border-color: #7f1d1d; color: #fecaca; }

  /* ── STAT GRID ── */
  .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 1.5rem; }
  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
  }
  .stat-num   { font-size: 26px; font-weight: 600; }
  .stat-label { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .stat-blue   { color: var(--accent); }
  .stat-green  { color: var(--success); }
  .stat-amber  { color: var(--warn); }
  .stat-purple { color: #a78bfa; }

  /* ── BUTTONS ── */
  .btn {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--font);
    font-size: 13px;
    font-weight: 500;
    padding: 7px 14px;
    border-radius: 7px;
    border: 1px solid var(--border);
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s;
    background: var(--surface2);
    color: var(--text);
  }
  .btn:hover  { border-color: #2a3f5f; background: #1a2840; }
  .btn-primary {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }
  .btn-primary:hover { background: #2563eb; border-color: #2563eb; }
  .btn-success {
    background: var(--success);
    border-color: var(--success);
    color: #fff;
  }
  .btn-success:hover { background: #059669; }
  .btn-sm { font-size: 12px; padding: 5px 10px; }
  .btn-danger { background: #3b0a0a; border-color: var(--danger); color: #fca5a5; }
  .btn-danger:hover { background: #4c0e0e; }

  /* ── FORMS ── */
  .form-group { margin-bottom: 1rem; }
  label { display: block; font-size: 13px; font-weight: 500; color: var(--muted2); margin-bottom: 6px; }
  input[type="text"], input[type="date"], textarea, select {
    width: 100%;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-family: var(--font);
    font-size: 14px;
    padding: 9px 12px;
    outline: none;
    transition: border-color 0.15s;
  }
  input:focus, textarea:focus, select:focus { border-color: var(--accent); }
  input::placeholder, textarea::placeholder { color: var(--muted); }
  textarea { resize: vertical; min-height: 80px; }

  /* ── MISC ── */
  h1 { font-size: 22px; font-weight: 600; margin-bottom: 0.25rem; }
  .subtitle { color: var(--muted2); font-size: 13px; margin-bottom: 1.5rem; }
  hr { border: none; border-top: 1px solid var(--border); margin: 1.25rem 0; }
  .empty-state { text-align: center; padding: 3rem 1rem; color: var(--muted); }
  .empty-state .emoji { font-size: 36px; margin-bottom: 0.75rem; }
  .action-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.5rem; }
  .section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 8px;
  }
  .delete-link { font-size: 12px; color: var(--muted); text-decoration: none; }
  .delete-link:hover { color: var(--danger); }
  .note-form { display: flex; gap: 6px; margin-top: 6px; }
  .note-form input { flex: 1; font-size: 13px; padding: 6px 10px; }
  .note-text { font-size: 12px; color: var(--muted2); font-style: italic; margin-top: 4px; }
</style>
</head>
<body>
<nav>
  <a class="nav-brand" href="/">Goal<span>Flow</span></a>
  <div class="nav-links">
    <a href="/">Dashboard</a>
    <a href="/review">Daily Review</a>
    <a href="/create">+ New Goal</a>
  </div>
</nav>
<div class="page">
  {% block content %}{% endblock %}
</div>
</body>
</html>
"""

# ─────────────────────────────────────────
# HOME
# ─────────────────────────────────────────

HOME_TMPL = BASE.replace("{% block content %}{% endblock %}", """
{% block content %}
{% set total_goals = goals|length %}
{% set total_tasks = goals|sum(attribute='tasks')|list|length %}
{% set done_tasks  = goals|map(attribute='tasks')|sum(start=[])|selectattr('completed')|list|length %}

<h1>Dashboard</h1>
<p class="subtitle">Track your goals and stay accountable every day.</p>

<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-num stat-blue">{{ total_goals }}</div>
    <div class="stat-label">Active Goals</div>
  </div>
  <div class="stat-card">
    <div class="stat-num stat-green">{{ done_tasks }}</div>
    <div class="stat-label">Tasks Done</div>
  </div>
  <div class="stat-card">
    <div class="stat-num stat-amber">{{ total_tasks - done_tasks }}</div>
    <div class="stat-label">Remaining</div>
  </div>
  <div class="stat-card">
    <div class="stat-num stat-purple">
      {{ ((done_tasks / total_tasks * 100)|round|int if total_tasks else 0) }}%
    </div>
    <div class="stat-label">Overall Progress</div>
  </div>
</div>

<div class="action-row">
  <a href="/create" class="btn btn-primary">＋ New Goal</a>
  <a href="/review" class="btn">📋 Daily Review</a>
</div>

{% if not goals %}
<div class="empty-state">
  <div class="emoji">🎯</div>
  <p>No goals yet. Create your first one to get started.</p>
</div>
{% endif %}

{% for g in goals %}
{% set fb = g.feedback %}
{% set pct = fb.pct %}
<div class="card">
  <div class="card-header">
    <div>
      <div class="card-title">{{ g.goal }}</div>
      <div class="card-meta">
        Created {{ g.created[:10] }}
        {% if g.timeframe %} · Due {{ g.timeframe }}{% endif %}
        {% if g.category %} · {{ g.category|title }}{% endif %}
      </div>
    </div>
    <div style="display:flex; gap:6px; align-items:center;">
      <a href="/review/{{ g.id }}" class="btn btn-sm">Review</a>
      <a href="/delete/{{ g.id }}" class="delete-link" onclick="return confirm('Delete this goal?')">✕</a>
    </div>
  </div>

  <div class="progress-wrap">
    <div class="progress-label">
      <span>Progress</span>
      <span>{{ fb.done }}/{{ fb.total }} tasks · {{ pct }}%</span>
    </div>
    <div class="progress-bar-bg">
      <div class="progress-bar-fill" style="width:{{ pct }}%"></div>
    </div>
  </div>

  <div class="task-list">
  {% for t in g.tasks %}
    <div class="task-row {% if t.completed %}done{% endif %}">
      <a href="/toggle/{{ g.id }}/{{ loop.index0 }}" class="check-btn" style="text-decoration:none;">✓</a>
      <span class="task-text">{{ t.task }}</span>
      <div class="badges">
        <span class="badge badge-{{ t.priority }}">{{ t.priority }}</span>
        <span class="badge badge-{{ t.frequency }}">{{ t.frequency }}</span>
        <span class="badge badge-{{ t.difficulty }}">{{ t.difficulty }}</span>
      </div>
    </div>
  {% endfor %}
  </div>
</div>
{% endfor %}
{% endblock %}
""")


# ─────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────

CREATE_TMPL = BASE.replace("{% block content %}{% endblock %}", """
{% block content %}
<h1>New Goal</h1>
<p class="subtitle">Define your goal and let the AI build your action plan.</p>

<div class="card">
  <form method="post" action="/create">
    <div class="form-group">
      <label>What is your goal?</label>
      <input type="text" name="goal" placeholder='e.g. "Score 750 on the GMAT" or "Get fit for summer"' required>
    </div>
    <div class="form-group">
      <label>Target deadline (optional)</label>
      <input type="date" name="timeframe">
    </div>
    <div class="form-group">
      <label>Extra context (optional)</label>
      <textarea name="context" placeholder='e.g. "Currently scoring around 600, can study 1hr/day"'></textarea>
    </div>
    <button type="submit" class="btn btn-primary" style="width:100%; justify-content:center; padding:10px;">
      Generate Action Plan →
    </button>
  </form>
</div>
{% endblock %}
""")

# ─────────────────────────────────────────
# REVIEW (all goals)
# ─────────────────────────────────────────

REVIEW_TMPL = BASE.replace("{% block content %}{% endblock %}", """
{% block content %}
<h1>Daily Review</h1>
<p class="subtitle">Your accountability snapshot for {{ today }}.</p>

{% if not goals %}
<div class="empty-state">
  <div class="emoji">📋</div>
  <p>No goals to review. Create one first.</p>
</div>
{% endif %}

{% for g in goals %}
{% set fb = g.feedback %}
<div class="feedback-banner feedback-{{ fb.status }}">
  <span>{% if fb.status == 'success' %}✅{% elif fb.status == 'good' %}📈{% elif fb.status == 'warn' %}⚠️{% else %}🔴{% endif %}</span>
  <div>
    <strong>{{ g.goal }}</strong><br>
    <span style="font-size:13px;">{{ fb.message }}</span>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <div>
      <div class="card-title">{{ g.goal }}</div>
      <div class="card-meta">{{ fb.done }}/{{ fb.total }} complete · {{ fb.pct }}%</div>
    </div>
    <a href="/review/{{ g.id }}" class="btn btn-sm">Deep dive →</a>
  </div>

  {% set incomplete = g.tasks|rejectattr('completed')|list %}
  {% if incomplete %}
  <div class="section-label" style="margin-top:.5rem">Incomplete tasks</div>
  <div class="task-list">
    {% for t in incomplete %}
    <div class="task-row">
      <a href="/toggle/{{ g.id }}/{{ loop.index0 + (g.tasks|selectattr('completed')|list|length) }}" class="check-btn" style="text-decoration:none;">✓</a>
      <span class="task-text">{{ t.task }}</span>
      <div class="badges">
        <span class="badge badge-{{ t.priority }}">{{ t.priority }}</span>
        <span class="badge badge-{{ t.frequency }}">{{ t.frequency }}</span>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <p style="color: var(--success); font-size:14px; margin-top:.5rem;">🎉 All tasks complete!</p>
  {% endif %}
</div>
{% endfor %}
{% endblock %}
""")

# ─────────────────────────────────────────
# REVIEW — single goal deep dive
# ─────────────────────────────────────────

GOAL_REVIEW_TMPL = BASE.replace("{% block content %}{% endblock %}", """
{% block content %}
<div style="margin-bottom:1rem;">
  <a href="/review" class="btn btn-sm">← Back to review</a>
</div>

<h1>{{ g.goal }}</h1>
<p class="subtitle">
  Created {{ g.created[:10] }}
  {% if g.timeframe %} · Due {{ g.timeframe }}{% endif %}
  · Category: {{ g.category|title }}
</p>

<div class="feedback-banner feedback-{{ fb.status }}">
  <span>{% if fb.status == 'success' %}✅{% elif fb.status == 'good' %}📈{% elif fb.status == 'warn' %}⚠️{% else %}🔴{% endif %}</span>
  <span>{{ fb.message }}</span>
</div>

<div class="card">
  <div class="section-label">All tasks</div>
  <div class="task-list">
  {% for t in g.tasks %}
    <div>
      <div class="task-row {% if t.completed %}done{% endif %}">
        <a href="/toggle/{{ g.id }}/{{ loop.index0 }}" class="check-btn" style="text-decoration:none;">✓</a>
        <span class="task-text">{{ t.task }}</span>
        <div class="badges">
          <span class="badge badge-{{ t.priority }}">{{ t.priority }}</span>
          <span class="badge badge-{{ t.frequency }}">{{ t.frequency }}</span>
          <span class="badge badge-{{ t.difficulty }}">{{ t.difficulty }}</span>
        </div>
      </div>
      {% if t.note %}
      <div class="note-text" style="margin-left:30px;">📝 {{ t.note }}</div>
      {% endif %}
      <form class="note-form" method="post" action="/note/{{ g.id }}/{{ loop.index0 }}" style="margin-left:30px; margin-top:4px;">
        <input type="text" name="note" placeholder="Add a note…" value="{{ t.note }}">
        <button type="submit" class="btn btn-sm">Save</button>
      </form>
    </div>
  {% endfor %}
  </div>
</div>
{% endblock %}
""")


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

def enrich(goals):
    """Attach computed feedback to each goal for templates."""
    for g in goals:
        g["feedback"] = daily_feedback(g)
        if "category" not in g:
            g["category"] = detect_category(g.get("goal", ""))
    return goals


@app.route("/")
def home():
    data = load_data()
    goals = enrich(data["goals"])
    return render_template_string(HOME_TMPL, goals=goals)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data = load_data()
        goal_text = request.form.get("goal", "").strip()
        timeframe = request.form.get("timeframe", "")
        context   = request.form.get("context", "")

        tasks = generate_plan(goal_text, timeframe)
        new_goal = {
            "id":        next_id(data["goals"]),
            "goal":      goal_text,
            "timeframe": timeframe,
            "context":   context,
            "category":  detect_category(goal_text),
            "created":   datetime.now().isoformat(),
            "tasks":     tasks,
        }
        data["goals"].append(new_goal)
        save_data(data)
        return redirect("/")

    return render_template_string(CREATE_TMPL)


@app.route("/toggle/<int:gid>/<int:tid>")
def toggle(gid, tid):
    data = load_data()
    for g in data["goals"]:
        if g["id"] == gid and 0 <= tid < len(g["tasks"]):
            g["tasks"][tid]["completed"] = not g["tasks"][tid]["completed"]
    save_data(data)
    return redirect(request.referrer or "/")


@app.route("/delete/<int:gid>")
def delete(gid):
    data = load_data()
    data["goals"] = [g for g in data["goals"] if g["id"] != gid]
    save_data(data)
    return redirect("/")


@app.route("/review")
def review():
    data = load_data()
    goals = enrich(data["goals"])
    today = date.today().strftime("%B %d, %Y")
    return render_template_string(REVIEW_TMPL, goals=goals, today=today)


@app.route("/review/<int:gid>")
def review_goal(gid):
    data = load_data()
    g = next((x for x in data["goals"] if x["id"] == gid), None)
    if not g:
        return redirect("/review")
    g["category"] = g.get("category") or detect_category(g["goal"])
    fb = daily_feedback(g)
    return render_template_string(GOAL_REVIEW_TMPL, g=g, fb=fb)


@app.route("/note/<int:gid>/<int:tid>", methods=["POST"])
def add_note(gid, tid):
    data = load_data()
    note = request.form.get("note", "").strip()
    for g in data["goals"]:
        if g["id"] == gid and 0 <= tid < len(g["tasks"]):
            g["tasks"][tid]["note"] = note
    save_data(data)
    return redirect(f"/review/{gid}")


# ─────────────────────────────────────────
# API (bonus — for future frontend use)
# ─────────────────────────────────────────

@app.route("/api/goals")
def api_goals():
    data = load_data()
    return jsonify(data["goals"])


@app.route("/api/goals/<int:gid>/progress")
def api_progress(gid):
    data = load_data()
    g = next((x for x in data["goals"] if x["id"] == gid), None)
    if not g:
        return jsonify({"error": "Not found"}), 404
    return jsonify(daily_feedback(g))


# ─────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────

def run_tests():
    print("Running tests…")
    assert isinstance(load_data(), dict)

    tasks = _generic_tasks("learn chess")
    assert len(tasks) == 6

    plan = generate_plan("learn python")
    assert isinstance(plan, list) and len(plan) > 0
    assert all(k in plan[0] for k in ("task", "frequency", "difficulty", "priority"))

    assert detect_category("study for the GMAT") == "study"
    assert detect_category("get fit") == "fitness"
    assert detect_category("learn Spanish") == "language"
    assert detect_category("random thing") == "general"

    fb = daily_feedback({"tasks": [{"completed": True}, {"completed": False}]})
    assert "pct" in fb and fb["pct"] == 50

    print("All tests passed ✓")


# ─────────────────────────────────────────
# ENTRY
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("GoalFlow loaded.")
    print("Local:  python app.py  →  then open http://localhost:5000")
    print("Render: gunicorn app:app")
