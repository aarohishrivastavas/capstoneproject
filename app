<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Momentum · Study Planner</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400;500&family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet" />

<style>
/* ═══════════════════════════════════════
   TOKENS
═══════════════════════════════════════ */
:root {
  --ivory:     #f7f4ef;
  --cream:     #edeae2;
  --paper:     #ffffff;
  --ink:       #1c1917;
  --ink-2:     #44403c;
  --ink-3:     #78716c;
  --ink-4:     #a8a29e;
  --forest:    #2d5a3d;
  --forest-2:  #3d7a54;
  --forest-3:  #c4dccb;
  --forest-4:  #eef6f1;
  --amber:     #92400e;
  --amber-bg:  #fef3c7;
  --amber-bd:  #fcd34d;
  --rose:      #9f1239;
  --rose-bg:   #fff1f2;
  --rose-bd:   #fda4af;
  --border:    #e2ddd8;
  --radius:    16px;
  --shadow:    0 1px 3px rgba(28,25,23,.06), 0 4px 14px rgba(28,25,23,.05);
  --shadow-lg: 0 8px 32px rgba(28,25,23,.10), 0 2px 6px rgba(28,25,23,.06);
}

/* ═══════════════════════════════════════
   RESET & BASE
═══════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--ivory);
  color: var(--ink);
  font-family: 'Lato', sans-serif;
  font-weight: 300;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* subtle grain overlay */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

/* ═══════════════════════════════════════
   LAYOUT
═══════════════════════════════════════ */
.wrap {
  position: relative; z-index: 1;
  max-width: 680px;
  margin: 0 auto;
  padding: 3rem 1.5rem 6rem;
}

/* ═══════════════════════════════════════
   HEADER
═══════════════════════════════════════ */
.header {
  text-align: center;
  padding-bottom: 44px;
  animation: fadeUp .6s ease both;
}
.eyebrow {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 3.5px;
  text-transform: uppercase;
  color: var(--ink-4);
  margin-bottom: 14px;
}
h1 {
  font-family: 'Libre Baskerville', Georgia, serif;
  font-size: clamp(40px, 7vw, 58px);
  font-weight: 400;
  color: var(--ink);
  letter-spacing: -2px;
  line-height: 1.05;
  margin-bottom: 12px;
}
h1 em { font-style: italic; color: var(--forest); }
.rule {
  width: 36px; height: 1px;
  background: var(--border);
  margin: 0 auto;
}

/* ═══════════════════════════════════════
   SECTION LABEL
═══════════════════════════════════════ */
.label {
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--ink-4);
  display: block;
  margin: 24px 0 6px;
}

/* ═══════════════════════════════════════
   CARD
═══════════════════════════════════════ */
.card {
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

/* ═══════════════════════════════════════
   API KEY BANNER
═══════════════════════════════════════ */
.key-banner {
  padding: 18px 22px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  animation: fadeUp .5s .1s ease both;
}
.key-icon {
  font-size: 20px;
  flex-shrink: 0;
}
.key-text { flex: 1; min-width: 180px; }
.key-text strong {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 2px;
}
.key-text span {
  font-size: 12px;
  color: var(--ink-4);
}
.key-text a { color: var(--forest); text-decoration: none; }
.key-text a:hover { text-decoration: underline; }
.key-input-wrap { display: flex; gap: 8px; width: 100%; margin-top: 10px; }
#apiKeyInput {
  flex: 1;
  font-family: 'DM Mono', monospace;
  font-size: 12.5px;
  letter-spacing: 0.5px;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--ivory);
  color: var(--ink);
  outline: none;
  transition: border-color .15s, box-shadow .15s;
}
#apiKeyInput:focus {
  border-color: var(--forest);
  box-shadow: 0 0 0 3px rgba(45,90,61,.1);
}
.key-saved {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 1px;
  color: var(--forest);
  text-transform: uppercase;
  padding: 4px 10px;
  background: var(--forest-4);
  border: 1px solid var(--forest-3);
  border-radius: 100px;
  white-space: nowrap;
  align-self: center;
  opacity: 0;
  transition: opacity .3s;
}
.key-saved.show { opacity: 1; }

/* ═══════════════════════════════════════
   FORM
═══════════════════════════════════════ */
#formSection { animation: fadeUp .5s .15s ease both; }

input[type="text"], input[type="date"], textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--paper);
  color: var(--ink);
  font-family: 'Lato', sans-serif;
  font-size: 14px;
  font-weight: 300;
  outline: none;
  transition: border-color .15s, box-shadow .15s;
  box-shadow: 0 1px 2px rgba(28,25,23,.04);
}
input:focus, textarea:focus {
  border-color: var(--forest);
  box-shadow: 0 0 0 3px rgba(45,90,61,.1);
}
input::placeholder, textarea::placeholder {
  color: var(--ink-4);
}
textarea { resize: vertical; line-height: 1.6; }

.row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

/* range slider */
.slider-wrap { display: flex; align-items: center; gap: 12px; }
input[type="range"] {
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  border-radius: 100px;
  background: var(--cream);
  border: none;
  box-shadow: none;
  padding: 0;
  cursor: pointer;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--forest);
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(45,90,61,.3);
  transition: transform .15s;
}
input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.15); }
.slider-val {
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--forest);
  min-width: 36px;
  text-align: right;
}

/* ═══════════════════════════════════════
   GENERATE BUTTON
═══════════════════════════════════════ */
.btn {
  display: block;
  width: 100%;
  margin-top: 28px;
  padding: 14px 32px;
  background: var(--ink);
  color: #fafaf8;
  border: none;
  border-radius: 100px;
  font-family: 'Lato', sans-serif;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(28,25,23,.18);
  transition: background .2s, box-shadow .2s, transform .15s;
}
.btn:hover {
  background: var(--forest);
  box-shadow: 0 6px 20px rgba(45,90,61,.28);
  transform: translateY(-1px);
}
.btn:active { transform: translateY(0); }
.btn:disabled {
  opacity: .5;
  cursor: not-allowed;
  transform: none;
}

/* ═══════════════════════════════════════
   ERROR
═══════════════════════════════════════ */
.error-msg {
  margin-top: 12px;
  padding: 11px 16px;
  background: var(--rose-bg);
  border: 1px solid var(--rose-bd);
  border-radius: 10px;
  font-size: 13px;
  color: var(--rose);
  display: none;
}
.error-msg.show { display: block; }

/* ═══════════════════════════════════════
   LOADING
═══════════════════════════════════════ */
.loader {
  display: none;
  text-align: center;
  padding: 48px 0;
  animation: fadeUp .3s ease both;
}
.loader.show { display: block; }
.dots span {
  display: inline-block;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--forest);
  margin: 0 3px;
  animation: bounce .9s ease-in-out infinite;
}
.dots span:nth-child(2) { animation-delay: .15s; }
.dots span:nth-child(3) { animation-delay: .3s; }
@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: .4; }
  40%            { transform: translateY(-10px); opacity: 1; }
}
.loader p {
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--ink-4);
  margin-top: 18px;
}

/* ═══════════════════════════════════════
   PLAN SECTION
═══════════════════════════════════════ */
#planSection { display: none; }
#planSection.show { display: block; animation: fadeUp .5s ease both; }

/* countdown */
.countdown {
  padding: 24px 28px;
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.c-num {
  font-family: 'Libre Baskerville', serif;
  font-size: 64px;
  font-weight: 700;
  color: var(--forest);
  line-height: 1;
  letter-spacing: -3px;
  flex-shrink: 0;
}
.c-sub {
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--ink-4);
  margin-top: 5px;
}
.c-right { flex: 1; min-width: 180px; }
.c-goal {
  font-family: 'Libre Baskerville', serif;
  font-size: 20px;
  font-style: italic;
  font-weight: 400;
  color: var(--ink);
  margin-bottom: 10px;
  line-height: 1.35;
}
.chips { display: flex; gap: 7px; flex-wrap: wrap; }
.chip {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  padding: 4px 12px;
  border-radius: 100px;
  background: var(--forest-4);
  color: var(--forest);
  border: 1px solid var(--forest-3);
}
.chip.amber { background: var(--amber-bg); color: var(--amber); border-color: var(--amber-bd); }
.chip.rose  { background: var(--rose-bg);  color: var(--rose);  border-color: var(--rose-bd); }

/* timeline */
.timeline { padding: 16px 20px; margin-bottom: 22px; }
.tl-labels {
  display: flex;
  justify-content: space-between;
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  color: var(--ink-4);
  margin-bottom: 10px;
}
.tl-track { background: var(--cream); border-radius: 100px; height: 4px; overflow: hidden; }
.tl-fill  { height: 100%; border-radius: 100px; transition: width .6s ease; }

/* starting position */
.sp-card {
  background: var(--forest-4);
  border: 1px solid var(--forest-3);
  border-left: 3px solid var(--forest);
  border-radius: 0 14px 14px 0;
  padding: 14px 18px;
  margin-bottom: 18px;
}
.sp-label {
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--forest);
  margin-bottom: 5px;
}
.sp-text { font-size: 13.5px; color: var(--ink-2); line-height: 1.65; font-weight: 300; }

/* divider */
.divider {
  display: flex; align-items: center; gap: 16px;
  margin: 28px 0 20px;
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--ink-4);
}
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* task cards */
.task {
  padding: 18px 20px;
  margin-bottom: 9px;
  position: relative;
  overflow: hidden;
  transition: box-shadow .2s, transform .15s;
  cursor: default;
}
.task:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-1px);
}
.task::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
}
.task.pri-high::before  { background: var(--rose); }
.task.pri-medium::before{ background: var(--amber); }
.task.pri-low::before   { background: var(--forest); }
.task.done { opacity: .45; }

.t-day {
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--ink-4);
  margin-bottom: 6px;
}
.t-name {
  font-family: 'Libre Baskerville', serif;
  font-size: 16px;
  font-weight: 400;
  color: var(--ink);
  margin-bottom: 12px;
  line-height: 1.5;
}
.task.done .t-name { text-decoration: line-through; color: var(--ink-4); }
.t-footer { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.t-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag {
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 100px;
  white-space: nowrap;
}
.tag-easy { background: var(--forest-4); color: var(--forest); border: 1px solid var(--forest-3); }
.tag-med  { background: var(--amber-bg); color: var(--amber);  border: 1px solid var(--amber-bd); }
.tag-hard { background: var(--rose-bg);  color: var(--rose);   border: 1px solid var(--rose-bd); }
.tag-freq { background: var(--cream);    color: var(--ink-3);  border: 1px solid var(--border); }

/* checkbox */
.check-wrap {
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; user-select: none;
}
.check-wrap input[type="checkbox"] {
  width: 16px; height: 16px;
  border: 1.5px solid var(--border);
  border-radius: 4px;
  accent-color: var(--forest);
  cursor: pointer;
  flex-shrink: 0;
}
.check-wrap span {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--ink-4);
}

/* progress */
.progress {
  padding: 22px 26px;
  margin: 22px 0;
  display: flex;
  align-items: center;
  gap: 22px;
}
.p-nums {
  font-family: 'Libre Baskerville', serif;
  font-size: 46px;
  font-weight: 700;
  color: var(--forest);
  line-height: 1;
  letter-spacing: -2px;
  flex-shrink: 0;
}
.p-nums small {
  font-size: 22px;
  color: var(--ink-4);
  font-weight: 400;
  letter-spacing: -1px;
}
.p-sub {
  font-family: 'DM Mono', monospace;
  font-size: 9.5px;
  color: var(--ink-4);
  letter-spacing: 1px;
  margin-top: 4px;
}
.p-bar-outer { flex: 1; background: var(--cream); border-radius: 100px; height: 5px; overflow: hidden; }
.p-bar-inner {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--forest), var(--forest-2));
  transition: width .5s ease;
}
.p-pct {
  font-family: 'Libre Baskerville', serif;
  font-size: 30px;
  font-weight: 700;
  color: var(--forest);
  letter-spacing: -1px;
  flex-shrink: 0;
}

/* success */
.success {
  background: var(--forest-4);
  border: 1px solid var(--forest-3);
  border-radius: var(--radius);
  padding: 22px 28px;
  text-align: center;
  margin-top: 16px;
  display: none;
}
.success.show { display: block; animation: fadeUp .4s ease both; }
.success p {
  font-family: 'Libre Baskerville', serif;
  font-size: 22px;
  font-style: italic;
  color: var(--forest);
}

/* restart */
.btn-ghost {
  display: block;
  width: 100%;
  margin-top: 18px;
  padding: 12px 32px;
  background: transparent;
  color: var(--ink-3);
  border: 1px solid var(--border);
  border-radius: 100px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all .2s;
}
.btn-ghost:hover {
  border-color: var(--ink-3);
  color: var(--ink);
  background: var(--cream);
}

/* ═══════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════ */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ═══════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════ */
@media (max-width: 540px) {
  .wrap { padding: 2rem 1rem 5rem; }
  .row-2 { grid-template-columns: 1fr; }
  .countdown { gap: 14px; }
  .c-num { font-size: 48px; }
}
</style>
</head>

<body>
<div class="wrap">

  <!-- HEADER -->
  <header class="header">
    <div class="eyebrow">Study Planner · Gemini 2.0</div>
    <h1>Build <em>momentum.</em></h1>
    <div class="rule"></div>
  </header>

  <!-- API KEY BANNER -->
  <div class="card key-banner">
    <div class="key-icon">🔑</div>
    <div class="key-text" style="flex:1;min-width:200px;">
      <strong>Gemini API Key</strong>
      <span>Stored only in this tab's memory. Get yours free at
        <a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com</a>
      </span>
      <div class="key-input-wrap">
        <input type="password" id="apiKeyInput" placeholder="AIza..." autocomplete="off" />
        <span class="key-saved" id="keySaved">✓ Saved</span>
      </div>
    </div>
  </div>

  <!-- FORM -->
  <div id="formSection">
    <span class="label">Main Goal</span>
    <input type="text" id="goal" placeholder="e.g. Score 1400+ on the SAT" />

    <span class="label">Target Result</span>
    <input type="text" id="endGoal" placeholder="e.g. Consistently hit 1400 across two practice tests" />

    <span class="label">Starting Position</span>
    <textarea id="startPos" rows="3" placeholder="e.g. Currently scoring ~1100. Reading: 580, Math: 520. Have Khan Academy. Studying weekday evenings ~2 hrs."></textarea>

    <div class="row-2">
      <div>
        <span class="label">Hard Deadline</span>
        <input type="date" id="deadline" />
      </div>
      <div>
        <span class="label">Study Hours / Day: <span id="hoursVal">2.0</span></span>
        <div class="slider-wrap" style="margin-top:8px;">
          <input type="range" id="hours" min="0.5" max="8" step="0.5" value="2" />
          <span class="slider-val" id="hoursDisplay">2.0 hrs</span>
        </div>
      </div>
    </div>

    <span class="label">Extra Context (optional)</span>
    <textarea id="context" rows="2" placeholder="e.g. Test anxiety, prefer videos, already finished algebra review"></textarea>

    <div class="error-msg" id="errorMsg"></div>
    <button class="btn" id="generateBtn" onclick="handleGenerate()">Generate Study Plan</button>
  </div>

  <!-- LOADER -->
  <div class="loader" id="loader">
    <div class="dots">
      <span></span><span></span><span></span>
    </div>
    <p>Building your plan…</p>
  </div>

  <!-- PLAN -->
  <div id="planSection">
    <!-- countdown injected here -->
    <div id="startPosRecap"></div>
    <div class="divider">Study Plan</div>
    <div id="taskList"></div>
    <div class="card progress">
      <div>
        <div class="p-nums" id="pNums">0<small>/0</small></div>
        <div class="p-sub">complete</div>
      </div>
      <div class="p-bar-outer"><div class="p-bar-inner" id="pBar" style="width:0%"></div></div>
      <div class="p-pct" id="pPct">0%</div>
    </div>
    <div class="success" id="successBanner">
      <p>All done — goal achieved.</p>
    </div>
    <button class="btn-ghost" onclick="restart()">↺ Start Over</button>
  </div>

</div><!-- /wrap -->

<script>
/* ─── State ─── */
let state = { tasks: [], completed: {}, goal: '', endGoal: '', startPos: '', deadline: '', startDate: '' };

/* ─── API key feedback ─── */
document.getElementById('apiKeyInput').addEventListener('input', function() {
  const saved = document.getElementById('keySaved');
  saved.classList.toggle('show', this.value.trim().length > 10);
});

/* ─── Slider ─── */
document.getElementById('hours').addEventListener('input', function() {
  document.getElementById('hoursVal').textContent    = parseFloat(this.value).toFixed(1);
  document.getElementById('hoursDisplay').textContent = parseFloat(this.value).toFixed(1) + ' hrs';
});

/* ─── Set default deadline (tomorrow) ─── */
(function() {
  const d = new Date(); d.setDate(d.getDate() + 14);
  document.getElementById('deadline').value = d.toISOString().split('T')[0];
  document.getElementById('deadline').min   = new Date(Date.now() + 86400000).toISOString().split('T')[0];
})();

/* ─── Helpers ─── */
function today()  { return new Date().toISOString().split('T')[0]; }
function daysBetween(a, b) {
  return Math.round((new Date(b) - new Date(a)) / 86400000);
}
function fmtDate(s) {
  return new Date(s + 'T12:00:00').toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' });
}
function showError(msg) {
  const el = document.getElementById('errorMsg');
  el.textContent = msg;
  el.classList.add('show');
}
function clearError() { document.getElementById('errorMsg').classList.remove('show'); }

/* ─── Generate ─── */
async function handleGenerate() {
  clearError();
  const apiKey   = document.getElementById('apiKeyInput').value.trim();
  const goal     = document.getElementById('goal').value.trim();
  const endGoal  = document.getElementById('endGoal').value.trim();
  const startPos = document.getElementById('startPos').value.trim();
  const deadline = document.getElementById('deadline').value;
  const hours    = document.getElementById('hours').value;
  const context  = document.getElementById('context').value.trim();

  if (!apiKey)    return showError('Paste your Gemini API key above first.');
  if (!goal)      return showError('Enter your main goal.');
  if (!endGoal)   return showError('Enter your target result.');
  if (!startPos)  return showError('Describe your starting position.');
  if (!deadline)  return showError('Pick a deadline.');
  if (deadline <= today()) return showError('Deadline must be in the future.');

  const daysLeft = daysBetween(today(), deadline);
  const n        = Math.min(daysLeft, 21);

  const prompt = `You are a focused study planner. Return ONLY valid JSON — no markdown, no explanation.

Goal: ${goal}
Target Result: ${endGoal}
Starting Position: ${startPos}
Deadline: ${fmtDate(deadline)} (${daysLeft} days away)
Study hours per day: ${hours}
Extra context: ${context || 'none'}

Create EXACTLY ${n} tasks, one per day.

{
  "tasks": [
    {
      "day": 1,
      "name": "Complete 30 Khan Academy algebra exercises focusing on linear equations",
      "frequency": "Daily",
      "difficulty": "Easy",
      "priority": "High"
    }
  ]
}

Rules:
- EXACTLY ${n} tasks
- Names: specific + measurable (include durations, topics, tools)
- difficulty: "Easy" | "Medium" | "Hard"
- priority: "High" | "Medium" | "Low"
- frequency: "Daily" | "3x/week" | "Weekly"
- Calibrate day 1 to starting position; build toward target result
- Valid JSON only`;

  // show loader
  document.getElementById('formSection').style.display = 'none';
  document.getElementById('loader').classList.add('show');
  document.getElementById('generateBtn').disabled = true;

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
      }
    );

    if (res.status === 400 || res.status === 401 || res.status === 403) {
      throw new Error('Invalid API key. Check and try again.');
    }
    if (!res.ok) throw new Error(`API error ${res.status}. Try again.`);

    const data = await res.json();
    const raw  = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    const clean = raw.replace(/```json|```/g, '').trim();
    const a = clean.indexOf('{'), b = clean.lastIndexOf('}');
    if (a === -1 || b === -1) throw new Error('Could not parse AI response. Try again.');

    const parsed = JSON.parse(clean.slice(a, b + 1));
    const tasks  = parsed.tasks || [];
    if (!tasks.length) throw new Error('No tasks returned. Try again.');

    // save state
    state = { tasks, completed: {}, goal, endGoal, startPos, deadline, startDate: today() };

    renderPlan();

  } catch (err) {
    document.getElementById('loader').classList.remove('show');
    document.getElementById('formSection').style.display = 'block';
    document.getElementById('generateBtn').disabled = false;
    showError(err.message || 'Something went wrong. Please try again.');
  }
}

/* ─── Render Plan ─── */
function renderPlan() {
  document.getElementById('loader').classList.remove('show');
  const plan = document.getElementById('planSection');
  plan.classList.add('show');

  const { tasks, deadline, startDate, endGoal, goal, startPos } = state;
  const todayStr = today();
  const daysLeft = daysBetween(todayStr, deadline);
  const totalDays = Math.max(daysBetween(startDate, deadline), 1);
  const elapsed   = Math.max(daysBetween(startDate, todayStr), 0);
  const pctEl     = Math.min(elapsed / totalDays * 100, 100);

  let barColor = '#2d5a3d', urgency = '';
  if (daysLeft <= 3) { barColor = '#9f1239'; urgency = '<span class="chip rose">⚑ Due soon</span>'; }
  else if (daysLeft <= 7) { barColor = '#92400e'; urgency = '<span class="chip amber">7 days left</span>'; }

  // inject countdown before startPosRecap's parent
  const existingCD = document.getElementById('countdownWrap');
  if (existingCD) existingCD.remove();

  const cdHTML = `
    <div id="countdownWrap">
      <div class="card countdown">
        <div>
          <div class="c-num">${Math.max(daysLeft,0)}</div>
          <div class="c-sub">days left</div>
        </div>
        <div class="c-right">
          <div class="c-goal">${endGoal}</div>
          <div class="chips">
            <span class="chip">◈ ${fmtDate(deadline)}</span>
            <span class="chip">${goal.slice(0,46)}</span>
            ${urgency}
          </div>
        </div>
      </div>
      <div class="card timeline">
        <div class="tl-labels">
          <span>Start · ${fmtDate(startDate)}</span>
          <span>${Math.max(100-pctEl,0).toFixed(0)}% remaining</span>
          <span>End · ${fmtDate(deadline)}</span>
        </div>
        <div class="tl-track">
          <div class="tl-fill" style="width:${pctEl.toFixed(1)}%;background:${barColor};"></div>
        </div>
      </div>
    </div>`;
  plan.insertAdjacentHTML('afterbegin', cdHTML);

  // starting position
  document.getElementById('startPosRecap').innerHTML = startPos ? `
    <div class="sp-card">
      <div class="sp-label">Starting Position</div>
      <div class="sp-text">${startPos}</div>
    </div>` : '';

  // tasks
  const list = document.getElementById('taskList');
  list.innerHTML = tasks.map((t, i) => {
    const diff = (t.difficulty || 'Easy').toLowerCase();
    const pri  = (t.priority   || 'Medium').toLowerCase();
    const diffCls = {easy:'tag-easy', medium:'tag-med', hard:'tag-hard'}[diff] || 'tag-med';
    const priCls  = {high:'pri-high',medium:'pri-medium',low:'pri-low'}[pri]    || 'pri-medium';
    const priTag  = {high:'tag-hard', medium:'tag-med',  low:'tag-easy'}[pri]   || 'tag-med';
    return `
      <div class="card task ${priCls}" id="task-${i}">
        <div class="t-day">Day ${t.day || i+1}</div>
        <div class="t-name">${t.name}</div>
        <div class="t-footer">
          <div class="t-tags">
            <span class="tag ${diffCls}">${t.difficulty}</span>
            <span class="tag ${priTag}">${t.priority} Priority</span>
            <span class="tag tag-freq">↻ ${t.frequency || 'Daily'}</span>
          </div>
          <label class="check-wrap">
            <input type="checkbox" onchange="toggleTask(${i}, this.checked)" />
            <span>Done</span>
          </label>
        </div>
      </div>`;
  }).join('');

  updateProgress();
}

/* ─── Toggle Task ─── */
function toggleTask(i, checked) {
  state.completed[i] = checked;
  const card = document.getElementById('task-' + i);
  card.classList.toggle('done', checked);
  updateProgress();
}

/* ─── Progress ─── */
function updateProgress() {
  const total = state.tasks.length;
  const done  = Object.values(state.completed).filter(Boolean).length;
  const pct   = total > 0 ? done / total : 0;

  document.getElementById('pNums').innerHTML = `${done}<small>/${total}</small>`;
  document.getElementById('pBar').style.width = (pct * 100).toFixed(1) + '%';
  document.getElementById('pPct').textContent  = Math.round(pct * 100) + '%';
  document.getElementById('successBanner').classList.toggle('show', pct === 1 && total > 0);
}

/* ─── Restart ─── */
function restart() {
  state = { tasks: [], completed: {}, goal:'', endGoal:'', startPos:'', deadline:'', startDate:'' };
  document.getElementById('planSection').classList.remove('show');
  document.getElementById('planSection').style.display = '';
  document.getElementById('formSection').style.display = 'block';
  document.getElementById('generateBtn').disabled = false;
  document.getElementById('taskList').innerHTML    = '';
  document.getElementById('startPosRecap').innerHTML = '';
  const cd = document.getElementById('countdownWrap');
  if (cd) cd.remove();
  clearError();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>
</body>
</html>
