"""
GoalFlow — AI Goal Dashboard
Deploy on Render with: gunicorn app:app

requirements.txt:
    flask
    gunicorn
    requests

Procfile:
    web: gunicorn app:app
"""

from flask import Flask, request, redirect, jsonify
import json
import os
import requests
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
# PLANNER
# ─────────────────────────────────────────

TASK_TEMPLATES = {
    "python": [
        {"task": "Learn core syntax: variables, loops, functions",       "frequency": "daily",  "difficulty": "easy",   "priority": "high"},
        {"task": "Complete 2 coding exercises on a practice platform",   "frequency": "daily",  "difficulty": "medium", "priority": "high"},
        {"task": "Build a small project applying what you have learned", "frequency": "weekly", "difficulty": "hard",   "priority": "high"},
        {"task": "Read one chapter of Python documentation",             "frequency": "daily",  "difficulty": "easy",   "priority": "medium"},
        {"task": "Review and refactor yesterday's code",                 "frequency": "daily",  "difficulty": "medium", "priority": "medium"},
        {"task": "Share or publish a project for feedback",              "frequency": "once",   "difficulty": "hard",   "priority": "low"},
    ],
    "fitness": [
        {"task": "Complete planned workout session",               "frequency": "daily",  "difficulty": "hard",   "priority": "high"},
        {"task": "Hit daily protein and calorie targets",          "frequency": "daily",  "difficulty": "medium", "priority": "high"},
        {"task": "Log workout metrics (reps, weight, time)",       "frequency": "daily",  "difficulty": "easy",   "priority": "high"},
        {"task": "30-minute active recovery or stretching",        "frequency": "weekly", "difficulty": "easy",   "priority": "medium"},
        {"task": "Review weekly progress and adjust plan",         "frequency": "weekly", "difficulty": "medium", "priority": "medium"},
        {"task": "Take progress photos for comparison",            "frequency": "weekly", "difficulty": "easy",   "priority": "low"},
    ],
    "study": [
        {"task": "Study core material for 45 focused minutes",       "frequency": "daily",  "difficulty": "hard",   "priority": "high"},
        {"task": "Review and annotate notes from previous session",  "frequency": "daily",  "difficulty": "medium", "priority": "high"},
        {"task": "Complete one practice test or problem set",        "frequency": "weekly", "difficulty": "hard",   "priority": "high"},
        {"task": "Create flashcards for key concepts",               "frequency": "daily",  "difficulty": "easy",   "priority": "medium"},
        {"task": "Identify and target weakest topic areas",          "frequency": "weekly", "difficulty": "medium", "priority": "medium"},
        {"task": "Summarize the week's learning in writing",         "frequency": "weekly", "difficulty": "medium", "priority": "low"},
    ],
    "language": [
        {"task": "Complete daily language lesson (app or textbook)", "frequency": "daily",  "difficulty": "medium", "priority": "high"},
        {"task": "Practice speaking or shadowing for 15 minutes",    "frequency": "daily",  "difficulty": "hard",   "priority": "high"},
        {"task": "Review vocabulary flashcards",                     "frequency": "daily",  "difficulty": "easy",   "priority": "high"},
        {"task": "Watch or listen to native content for 20 minutes", "frequency": "daily",  "difficulty": "easy",   "priority": "medium"},
        {"task": "Write a short paragraph in the target language",   "frequency": "weekly", "difficulty": "medium", "priority": "medium"},
        {"task": "Have a conversation session or language exchange",  "frequency": "weekly", "difficulty": "hard",   "priority": "medium"},
    ],
}

KEYWORD_MAP = {
    "python":   ["python", "coding", "programming", "developer", "code", "software"],
    "fitness":  ["gym", "fitness", "workout", "weight", "run", "muscle", "health", "exercise"],
    "study":    ["study", "school", "exam", "test", "gmat", "sat", "gre", "grade", "academic"],
    "language": ["language", "spanish", "french", "japanese", "mandarin", "german", "korean"],
}


def detect_category(goal):
    gl = (goal or "").lower()
    for cat, kws in KEYWORD_MAP.items():
        if any(k in gl for k in kws):
            return cat
    return "general"


def generate_plan(goal):
    if not isinstance(goal, str) or not goal.strip():
        return _generic_tasks("your goal")
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("No GROQ_API_KEY set, using fallback")
            return _generic_tasks(goal)
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{
                "role": "user",
                "content": f"""You are a goal planning assistant. Given this goal: {goal}

Return ONLY a valid JSON array of 6 tasks. Each task must have: task, frequency, difficulty, priority.
frequency: daily, weekly, or once
difficulty: easy, medium, or hard
priority: high, medium, or low

RESPOND WITH ONLY THE JSON ARRAY, NO OTHER TEXT."""
            }],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"Groq API error: {resp.status_code}, using fallback")
            return _generic_tasks(goal)
        
        content = resp.json()["choices"][0]["message"]["content"].strip()
        tasks = json.loads(content)
        for t in tasks:
            t["completed"] = False
            t["note"] = ""
        return tasks
    except Exception as e:
        print(f"LLM error: {e}, using fallback")
        return _generic_tasks(goal)


def _generic_tasks(goal):
    return [
        {"task": "Research and define a clear action plan for: " + goal, "frequency": "once",   "difficulty": "easy",   "priority": "high",   "completed": False, "note": ""},
        {"task": "Complete one focused session toward " + goal,          "frequency": "daily",  "difficulty": "medium", "priority": "high",   "completed": False, "note": ""},
        {"task": "Track progress and record results",                    "frequency": "daily",  "difficulty": "easy",   "priority": "high",   "completed": False, "note": ""},
        {"task": "Identify and address the biggest current obstacle",    "frequency": "weekly", "difficulty": "hard",   "priority": "medium", "completed": False, "note": ""},
        {"task": "Review the week and adjust your strategy",             "frequency": "weekly", "difficulty": "medium", "priority": "medium", "completed": False, "note": ""},
        {"task": "Reach a measurable milestone and document it",         "frequency": "once",   "difficulty": "hard",   "priority": "low",    "completed": False, "note": ""},
    ]


# ─────────────────────────────────────────
# FEEDBACK
# ─────────────────────────────────────────

def goal_feedback(goal_obj):
    tasks = goal_obj.get("tasks", [])
    total = len(tasks)
    done  = sum(1 for t in tasks if t.get("completed"))
    pct   = round((done / total) * 100) if total else 0

    high_inc = [t["task"] for t in tasks if not t.get("completed") and t.get("priority") == "high"]
    any_inc  = [t["task"] for t in tasks if not t.get("completed")]
    focus    = high_inc[0] if high_inc else (any_inc[0] if any_inc else "")

    if pct == 100:
        msg, status = "Outstanding — every task is complete. Consider raising the bar or adding stretch goals.", "success"
    elif pct >= 60:
        msg, status = "Solid progress at {}%. Focus next on: {}.".format(pct, focus), "good"
    elif pct >= 30:
        msg, status = "You're at {}% — momentum is building. Prioritize: {}.".format(pct, focus), "warn"
    else:
        msg, status = "Only {}% done. Start small — complete just one high-priority task today.".format(pct), "danger"

    return {"message": msg, "status": status, "pct": pct, "done": done, "total": total, "incomplete": any_inc}


def dashboard_stats(goals):
    total_tasks = sum(len(g.get("tasks", [])) for g in goals)
    done_tasks  = sum(sum(1 for t in g.get("tasks", []) if t.get("completed")) for g in goals)
    return {
        "total_goals": len(goals),
        "total_tasks": total_tasks,
        "done_tasks":  done_tasks,
        "remaining":   total_tasks - done_tasks,
        "overall_pct": round((done_tasks / total_tasks * 100)) if total_tasks else 0,
    }


# ─────────────────────────────────────────
# HTML HELPERS
# ─────────────────────────────────────────

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">'

CSS = """<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0f1e;--surf:#111827;--surf2:#1a2234;--bord:#1e2d45;--acc:#3b82f6;--acc2:#6366f1;--ok:#10b981;--warn:#f59e0b;--err:#ef4444;--txt:#f1f5f9;--mut:#64748b;--mut2:#94a3b8;--r:10px}
body{background:var(--bg);color:var(--txt);font-family:'DM Sans',sans-serif;font-size:15px;line-height:1.6;min-height:100vh}
a{color:inherit}
nav{background:var(--surf);border-bottom:1px solid var(--bord);padding:0 2rem;display:flex;align-items:center;justify-content:space-between;height:60px;position:sticky;top:0;z-index:100}
.brand{font-size:17px;font-weight:600;text-decoration:none;color:var(--txt)}.brand span{color:var(--acc)}
.nav-links{display:flex;gap:6px}.nav-links a{color:var(--mut2);text-decoration:none;font-size:13px;font-weight:500;padding:6px 12px;border-radius:6px;transition:background .15s,color .15s}.nav-links a:hover{background:var(--surf2);color:var(--txt)}
.page{max-width:860px;margin:0 auto;padding:2rem 1.5rem}
h1{font-size:22px;font-weight:600;margin-bottom:4px}
.sub{color:var(--mut2);font-size:13px;margin-bottom:1.5rem}
.card{background:var(--surf);border:1px solid var(--bord);border-radius:var(--r);padding:1.25rem 1.5rem;margin-bottom:1.25rem}
.ch{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1rem;gap:1rem}
.ct{font-size:16px;font-weight:600}.cm{font-size:12px;color:var(--mut);margin-top:3px;font-family:'DM Mono',monospace}
.pw{margin:.75rem 0}.pl{display:flex;justify-content:space-between;font-size:12px;color:var(--mut2);margin-bottom:5px}
.pb{background:var(--bord);border-radius:99px;height:6px;overflow:hidden}
.pf{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--acc),var(--acc2));transition:width .4s}
.tl{display:flex;flex-direction:column;gap:6px;margin-top:.75rem}
.tr{display:flex;align-items:center;gap:10px;background:var(--surf2);border:1px solid var(--bord);border-radius:8px;padding:10px 12px}
.tr.done .tt{text-decoration:line-through;color:var(--mut)}
.cb{width:20px;height:20px;min-width:20px;border-radius:5px;border:1.5px solid var(--mut);background:transparent;cursor:pointer;display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:11px;color:transparent;transition:background .15s,border-color .15s;flex-shrink:0}
.tr.done .cb{background:var(--ok);border-color:var(--ok);color:#fff}
.tt{flex:1;font-size:14px}
.bg-wrap{display:flex;gap:5px;flex-wrap:wrap}
.bg{font-size:11px;font-weight:500;padding:2px 8px;border-radius:99px;font-family:'DM Mono',monospace}
.bg-high{background:#3b1a1a;color:#fca5a5;border:1px solid #7f1d1d}
.bg-medium{background:#2d2007;color:#fcd34d;border:1px solid #78350f}
.bg-low{background:#0d2a1a;color:#6ee7b7;border:1px solid #065f46}
.bg-daily{background:#1a1f3a;color:#93c5fd;border:1px solid #1e3a6e}
.bg-weekly{background:#1f1a3a;color:#c4b5fd;border:1px solid #3b0764}
.bg-once{background:#1a2020;color:#67e8f9;border:1px solid #155e75}
.bg-easy{background:#0d2a1a;color:#86efac;border:1px solid #14532d}
.bg-hard{background:#3b1a1a;color:#fca5a5;border:1px solid #7f1d1d}
.bn{border-radius:var(--r);padding:12px 16px;font-size:14px;margin-bottom:1.25rem;border:1px solid;display:flex;gap:10px;align-items:flex-start}
.bn-success{background:#052e16;border-color:#14532d;color:#bbf7d0}
.bn-good{background:#0f172a;border-color:#1e3a6e;color:#bfdbfe}
.bn-warn{background:#1c1007;border-color:#78350f;color:#fde68a}
.bn-danger{background:#1a0505;border-color:#7f1d1d;color:#fecaca}
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1.5rem}
.sc{background:var(--surf);border:1px solid var(--bord);border-radius:var(--r);padding:1rem;text-align:center}
.sn{font-size:26px;font-weight:600}.sl{font-size:12px;color:var(--mut);margin-top:2px}
.cb-blue{color:var(--acc)}.cb-green{color:var(--ok)}.cb-amber{color:var(--warn)}.cb-purple{color:#a78bfa}
.btn{display:inline-flex;align-items:center;gap:6px;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;padding:7px 14px;border-radius:7px;border:1px solid var(--bord);cursor:pointer;text-decoration:none;background:var(--surf2);color:var(--txt);transition:all .15s}
.btn:hover{border-color:#2a3f5f;background:#1a2840}
.btn-p{background:var(--acc);border-color:var(--acc);color:#fff}.btn-p:hover{background:#2563eb;border-color:#2563eb}
.btn-sm{font-size:12px;padding:5px 10px}
.ar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:1.5rem}
.fg{margin-bottom:1rem}
label{display:block;font-size:13px;font-weight:500;color:var(--mut2);margin-bottom:6px}
input[type=text],input[type=date],textarea{width:100%;background:var(--surf2);border:1px solid var(--bord);border-radius:8px;color:var(--txt);font-family:'DM Sans',sans-serif;font-size:14px;padding:9px 12px;outline:none;transition:border-color .15s}
input:focus,textarea:focus{border-color:var(--acc)}
input::placeholder,textarea::placeholder{color:var(--mut)}
textarea{resize:vertical;min-height:80px}
.sl-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--mut);margin-bottom:8px}
.es{text-align:center;padding:3rem 1rem;color:var(--mut)}
.ei{font-size:36px;margin-bottom:.75rem}
.dl{font-size:12px;color:var(--mut);text-decoration:none;padding:4px 8px}.dl:hover{color:var(--err)}
.nr{display:flex;gap:6px;margin-top:6px;margin-left:30px}
.nr input{flex:1;font-size:13px;padding:6px 10px}
.nt{font-size:12px;color:var(--mut2);font-style:italic;margin-top:4px;margin-left:30px}
@media(max-width:600px){.sg{grid-template-columns:repeat(2,1fr)}nav{padding:0 1rem}.page{padding:1.25rem 1rem}}
</style>"""


def page(title, body):
    nav = """<nav>
  <a class="brand" href="/">Goal<span>Flow</span></a>
  <div class="nav-links">
    <a href="/">Dashboard</a>
    <a href="/review">Daily Review</a>
    <a href="/create">+ New Goal</a>
  </div>
</nav>"""
    return "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>GoalFlow &mdash; {t}</title>{f}{css}</head><body>{nav}<div class='page'>{body}</div></body></html>".format(
        t=title, f=FONTS, css=CSS, nav=nav, body=body)


def badges(task):
    p = task.get("priority", "medium")
    f = task.get("frequency", "daily")
    d = task.get("difficulty", "medium")
    return "<div class='bg-wrap'><span class='bg bg-{p}'>{p}</span><span class='bg bg-{f}'>{f}</span><span class='bg bg-{d}'>{d}</span></div>".format(p=p, f=f, d=d)


def task_row(gid, idx, task, back="/"):
    done  = "done" if task.get("completed") else ""
    check = "&#10003;" if task.get("completed") else ""
    note_val = task.get("note", "") or ""
    note_display = "<div class='nt'>&#128221; {}</div>".format(note_val) if note_val else ""
    note_form = """<form class='nr' method='post' action='/note/{gid}/{idx}?next={back}'>
  <input type='text' name='note' placeholder='Add a note&hellip;' value='{note}'>
  <button type='submit' class='btn btn-sm'>Save</button>
</form>""".format(gid=gid, idx=idx, back=back, note=note_val.replace("'", "&#39;"))

    return """<div>
  <div class='tr {done}'>
    <a href='/toggle/{gid}/{idx}?next={back}' class='cb'>{check}</a>
    <span class='tt'>{task}</span>
    {bg}
  </div>
  {nd}{nf}
</div>""".format(done=done, gid=gid, idx=idx, back=back,
                 check=check, task=task.get("task", ""),
                 bg=badges(task), nd=note_display, nf=note_form)


STATUS_ICON = {"success": "&#9989;", "good": "&#128200;", "warn": "&#9888;", "danger": "&#128308;"}


def goal_card(g, back="/"):
    fb  = goal_feedback(g)
    pct = fb["pct"]
    tf  = " &middot; Due {}".format(g["timeframe"]) if g.get("timeframe") else ""
    cat = g.get("category", "general").title()
    rows = "".join(task_row(g["id"], i, t, back) for i, t in enumerate(g.get("tasks", [])))

    return """<div class='card'>
  <div class='ch'>
    <div>
      <div class='ct'>{goal}</div>
      <div class='cm'>Created {created}{tf} &middot; {cat}</div>
    </div>
    <div style='display:flex;gap:6px;align-items:center;'>
      <a href='/review/{gid}' class='btn btn-sm'>Review</a>
      <a href='/delete/{gid}' class='dl' onclick="return confirm('Delete this goal?')">&#10005;</a>
    </div>
  </div>
  <div class='pw'>
    <div class='pl'><span>Progress</span><span>{done}/{total} tasks &middot; {pct}%</span></div>
    <div class='pb'><div class='pf' style='width:{pct}%'></div></div>
  </div>
  <div class='tl'>{rows}</div>
</div>""".format(goal=g.get("goal", ""), created=g.get("created", "")[:10],
                 tf=tf, cat=cat, gid=g["id"],
                 done=fb["done"], total=fb["total"], pct=pct, rows=rows)


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.route("/")
def home():
    data  = load_data()
    goals = data["goals"]
    stats = dashboard_stats(goals)

    sc = """<div class='sg'>
  <div class='sc'><div class='sn cb-blue'>{tg}</div><div class='sl'>Active Goals</div></div>
  <div class='sc'><div class='sn cb-green'>{dt}</div><div class='sl'>Tasks Done</div></div>
  <div class='sc'><div class='sn cb-amber'>{rem}</div><div class='sl'>Remaining</div></div>
  <div class='sc'><div class='sn cb-purple'>{pct}%</div><div class='sl'>Overall Progress</div></div>
</div>""".format(tg=stats["total_goals"], dt=stats["done_tasks"],
                 rem=stats["remaining"],  pct=stats["overall_pct"])

    ar = "<div class='ar'><a href='/create' class='btn btn-p'>&#xff0b; New Goal</a><a href='/review' class='btn'>&#128203; Daily Review</a></div>"

    if not goals:
        body = "<div class='es'><div class='ei'>&#127919;</div><p>No goals yet. <a href='/create' style='color:var(--acc)'>Create your first one.</a></p></div>"
    else:
        body = "".join(goal_card(g) for g in goals)

    content = "<h1>Dashboard</h1><p class='sub'>Track your goals and stay accountable every day.</p>" + sc + ar + body
    return page("Dashboard", content)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        data      = load_data()
        goal_text = request.form.get("goal", "").strip()
        timeframe = request.form.get("timeframe", "")
        context   = request.form.get("context", "")
        tasks     = generate_plan(goal_text)
        new_goal  = {
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

    form = """<div class='card'>
<form method='post' action='/create'>
  <div class='fg'><label>What is your goal?</label>
    <input type='text' name='goal' placeholder='e.g. &quot;Score 750 on the GMAT&quot; or &quot;Get fit for summer&quot;' required>
  </div>
  <div class='fg'><label>Target deadline (optional)</label>
    <input type='date' name='timeframe'>
  </div>
  <div class='fg'><label>Extra context (optional)</label>
    <textarea name='context' placeholder='e.g. &quot;Currently scoring around 600, can study 1hr/day&quot;'></textarea>
  </div>
  <button type='submit' class='btn btn-p' style='width:100%;justify-content:center;padding:10px;'>
    Generate Action Plan &rarr;
  </button>
</form>
</div>"""
    return page("New Goal", "<h1>New Goal</h1><p class='sub'>Define your goal and let the AI build your action plan.</p>" + form)


@app.route("/toggle/<int:gid>/<int:tid>")
def toggle(gid, tid):
    data = load_data()
    for g in data["goals"]:
        if g["id"] == gid and 0 <= tid < len(g["tasks"]):
            g["tasks"][tid]["completed"] = not g["tasks"][tid]["completed"]
    save_data(data)
    return redirect(request.args.get("next", "/"))


@app.route("/delete/<int:gid>")
def delete(gid):
    data = load_data()
    data["goals"] = [g for g in data["goals"] if g["id"] != gid]
    save_data(data)
    return redirect("/")


@app.route("/note/<int:gid>/<int:tid>", methods=["POST"])
def add_note(gid, tid):
    data = load_data()
    note = request.form.get("note", "").strip()
    for g in data["goals"]:
        if g["id"] == gid and 0 <= tid < len(g["tasks"]):
            g["tasks"][tid]["note"] = note
    save_data(data)
    return redirect(request.args.get("next", "/"))


@app.route("/review")
def review():
    data  = load_data()
    goals = data["goals"]
    today = date.today().strftime("%B %d, %Y")

    if not goals:
        body = "<div class='es'><div class='ei'>&#128203;</div><p>No goals to review. <a href='/create' style='color:var(--acc)'>Create one first.</a></p></div>"
    else:
        parts = []
        for g in goals:
            fb   = goal_feedback(g)
            icon = STATUS_ICON.get(fb["status"], "")
            banner = "<div class='bn bn-{s}'><span>{i}</span><div><strong>{goal}</strong><br><span style='font-size:13px'>{msg}</span></div></div>".format(
                s=fb["status"], i=icon, goal=g.get("goal",""), msg=fb["message"])

            incomplete = [(i, t) for i, t in enumerate(g.get("tasks", [])) if not t.get("completed")]
            if incomplete:
                rows = "".join(task_row(g["id"], i, t, back_url="/review") for i, t in incomplete)
                t_html = "<div class='sl-label' style='margin-top:.5rem'>Incomplete tasks</div><div class='tl'>" + rows + "</div>"
            else:
                t_html = "<p style='color:var(--ok);font-size:14px;margin-top:.5rem'>&#127881; All tasks complete!</p>"

            card = """<div class='card'>
  <div class='ch'>
    <div><div class='ct'>{goal}</div><div class='cm'>{done}/{total} complete &middot; {pct}%</div></div>
    <a href='/review/{gid}' class='btn btn-sm'>Deep dive &rarr;</a>
  </div>{t}
</div>""".format(goal=g.get("goal",""), done=fb["done"], total=fb["total"], pct=fb["pct"], gid=g["id"], t=t_html)
            parts.append(banner + card)
        body = "".join(parts)

    return page("Daily Review", "<h1>Daily Review</h1><p class='sub'>Your accountability snapshot for {}.</p>{}".format(today, body))


@app.route("/review/<int:gid>")
def review_goal(gid):
    data = load_data()
    g = next((x for x in data["goals"] if x["id"] == gid), None)
    if not g:
        return redirect("/review")

    g.setdefault("category", detect_category(g.get("goal", "")))
    fb   = goal_feedback(g)
    icon = STATUS_ICON.get(fb["status"], "")
    tf   = " &middot; Due {}".format(g["timeframe"]) if g.get("timeframe") else ""
    back = "/review/{}".format(gid)

    banner = "<div class='bn bn-{s}'><span>{i}</span><span>{msg}</span></div>".format(
        s=fb["status"], i=icon, msg=fb["message"])

    rows = "".join(task_row(g["id"], i, t, back) for i, t in enumerate(g.get("tasks", [])))
    card = "<div class='card'><div class='sl-label'>All tasks</div><div class='tl'>{}</div></div>".format(rows)

    content = """<div style='margin-bottom:1rem'><a href='/review' class='btn btn-sm'>&larr; Back</a></div>
<h1>{goal}</h1>
<p class='sub'>Created {created}{tf} &middot; {cat} &middot; {done}/{total} complete</p>
{banner}{card}""".format(
        goal=g.get("goal",""), created=g.get("created","")[:10],
        tf=tf, cat=g.get("category","general").title(),
        done=fb["done"], total=fb["total"],
        banner=banner, card=card)

    return page("Review", content)


# ─────────────────────────────────────────
# API
# ─────────────────────────────────────────

@app.route("/api/goals")
def api_goals():
    return jsonify(load_data()["goals"])


@app.route("/api/goals/<int:gid>/progress")
def api_progress(gid):
    g = next((x for x in load_data()["goals"] if x["id"] == gid), None)
    if not g:
        return jsonify({"error": "Not found"}), 404
    return jsonify(goal_feedback(g))


# ─────────────────────────────────────────
# ENTRY
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("GoalFlow loaded.")
    print("Local:  python app.py  ->  open http://localhost:5000")
    print("Render: gunicorn app:app")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
