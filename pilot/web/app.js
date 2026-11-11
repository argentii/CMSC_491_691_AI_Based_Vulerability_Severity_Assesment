/* Jev pilot dashboard. Vanilla JS, no build step. All data comes from /api/bundle;
   scores and noise floors come precomputed from the server (single source of truth: pilot/score.py). */
"use strict";

const ORDER_FALLBACK = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"];
// least -> most severe option letters per metric (mirrors SEV in pilot/web.py)
const SEV = { AV: "PLAN", AC: "HL", PR: "HLN", UI: "RN", S: "UC", C: "NLH", I: "NLH", A: "NLH" };
const METRIC_NAMES = {
  AV: "Attack Vector", AC: "Attack Complexity", PR: "Privileges Required", UI: "User Interaction",
  S: "Scope", C: "Confidentiality", I: "Integrity", A: "Availability",
};
const OPT_NAMES = {
  AV: { N: "network", A: "adjacent", L: "local", P: "physical" },
  AC: { L: "low", H: "high" },
  PR: { N: "none", L: "low", H: "high" },
  UI: { N: "none", R: "required" },
  S: { U: "unchanged", C: "changed" },
  C: { N: "none", L: "low", H: "high" },
  I: { N: "none", L: "low", H: "high" },
  A: { N: "none", L: "low", H: "high" },
};

const KINDS = ["neutral", "alarmist", "downplaying"];

let D = null; // bundle
let ORDER = ORDER_FALLBACK;

const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined) n.textContent = text;
  return n;
};
const fmt = (x, d = 2) => (x === null || x === undefined ? "–" : x.toFixed(d));
const sgn = (x, d = 2) => (x === null || x === undefined ? "–" : (x >= 0 ? "+" : "") + x.toFixed(d));

const bandClass = b => "band-" + (b || "none").toLowerCase();
function bandBadge(band, text) { return el("span", "badge " + bandClass(band), text ?? band); }

function rankColor(metric, letter) {
  const k = SEV[metric].length - 1;
  const i = SEV[metric].indexOf(letter);
  const ramp = ["var(--sev0)", "var(--sev1)", "var(--sev2)", "var(--sev3)"];
  return ramp[Math.round((i / k) * 3)] || "var(--muted)";
}

const letters = v => Object.fromEntries(v.split("/").slice(1).map(p => p.split(":")));

function renderVector(container, vector, cmpLetters) {
  const parts = letters(vector);
  for (const m of ORDER) {
    const chip = el("span", "mchip", `${m}:${parts[m]}`);
    chip.title = `${METRIC_NAMES[m]} = ${parts[m]}`;
    if (cmpLetters && cmpLetters[m] !== undefined && cmpLetters[m] !== parts[m]) chip.classList.add("diff");
    container.appendChild(chip);
  }
}

/* probability bars: one stacked row per run + a mean row */
function probBlock(metric, runs, meanProbs) {
  const wrap = el("div", "prob-block");
  wrap.appendChild(el("div", "prob-title", `${metric} · ${METRIC_NAMES[metric]}`));
  const opts = SEV[metric];
  const rows = runs.map(r => ({ label: "#" + (r.repeat ?? "?"), probs: r.probabilities[metric] || {} }));
  rows.push({ label: "mean", probs: meanProbs, mean: true });
  for (const row of rows) {
    const line = el("div", "prob-row" + (row.mean ? " mean" : ""));
    line.appendChild(el("span", "prob-label", row.label));
    const bar = el("div", "prob-bar");
    for (const o of opts) {
      const p = (row.probs && row.probs[o]) || 0;
      if (p <= 0.0005) continue;
      const seg = el("div", "prob-seg");
      seg.style.width = (p * 100).toFixed(1) + "%";
      seg.style.background = rankColor(metric, o);
      const name = OPT_NAMES[metric][o] || o;
      seg.title = `${name} (${o}): ${(p * 100).toFixed(0)}%`;
      if (p > 0.3) seg.textContent = Math.round(p * 100) + "% " + name;
      bar.appendChild(seg);
    }
    line.appendChild(bar);
    wrap.appendChild(line);
  }
  const legend = el("div", "prob-legend");
  for (const o of opts) {
    const sw = el("span", "legend-item");
    const i = el("i", "swatch");
    i.style.background = rankColor(metric, o);
    sw.appendChild(i);
    sw.appendChild(document.createTextNode(OPT_NAMES[metric][o] || o));
    legend.appendChild(sw);
  }
  wrap.appendChild(legend);
  return wrap;
}

/* ---------- Noise tab ---------- */
function renderNoise() {
  const tab = document.getElementById("tab-noise");
  tab.innerHTML = "";
  const cves = D.cves;
  const stable = cves.filter(c => c.stats && c.stats.distinct_vectors === 1).length;
  const spreads = cves.filter(c => c.stats).map(c => c.stats.max_prob_spread).sort((a, b) => a - b);
  const med = spreads.length ? spreads[Math.floor(spreads.length / 2)] : null;
  const nvdMatches = cves.filter(c => c.nvd_match);
  const fullMatch = nvdMatches.filter(c => c.nvd_match.n === ORDER.length).length;

  tab.appendChild(el("h2", null, `Noise test — identical description, ${D.meta.repeats} runs each`));
  const chips = el("div", "chips");
  for (const [k, v] of [["stable full vector", `${stable}/${cves.length}`],
                        ["median max prob spread", fmt(med)],
                        ["exact match vs NVD (all 8 metrics)", `${fullMatch}/${nvdMatches.length || "–"}`],
                        ["errors / invalid", cves.reduce((a, c) => a + (c.errors || 0), 0)]]) {
    const ch = el("div", "chip");
    ch.appendChild(el("b", null, String(v)));
    ch.appendChild(el("span", null, k));
    chips.appendChild(ch);
  }
  tab.appendChild(chips);

  const table = el("table", "grid");
  const head = el("tr");
  for (const h of ["CVE", "NVD", "Runs", "Err", "Same vector", "Metrics < 100% agreement",
                   "Jev score range", "Bands", "Max spread", "vs NVD"]) head.appendChild(el("th", null, h));
  table.appendChild(head);
  for (const c of cves) {
    const tr = el("tr", "row-click");
    tr.onclick = () => showDetail(c.cve_id);
    tr.appendChild(el("td", null, c.cve_id));
    tr.appendChild(el("td")).appendChild(bandBadge(c.nvd_band, String(c.nvd_score)));
    tr.appendChild(el("td", null, String((c.noise_runs || []).length)));
    tr.appendChild(el("td", c.errors ? "err" : null, String(c.errors || 0)));
    if (!c.stats) {
      for (let i = 0; i < 6; i++) tr.appendChild(el("td", null, "–"));
    } else {
      const s = c.stats;
      tr.appendChild(el("td", s.distinct_vectors === 1 ? "good" : "warn",
        s.distinct_vectors === 1 ? "yes" : `no (${s.distinct_vectors} distinct)`));
      const low = ORDER.filter(m => s.agreement[m] < 1).map(m => `${m} ${Math.round(s.agreement[m] * s.n)}/${s.n}`);
      tr.appendChild(el("td", null, low.join(", ") || "–"));
      tr.appendChild(el("td", null, `${s.score_lo}–${s.score_hi}`));
      tr.appendChild(el("td", null, s.bands.join(", ")));
      tr.appendChild(el("td", null, fmt(s.max_prob_spread)));
      const nm = c.nvd_match;
      tr.appendChild(el("td", nm.n === ORDER.length ? "good" : null,
        `${nm.n}/${nm.of}${nm.diff.length ? " · diff " + nm.diff.join(",") : ""}`));
    }
    table.appendChild(tr);
  }
  tab.appendChild(table);
  tab.appendChild(el("p", "hint", "Click a CVE row for per-run detail. Chip colours run least → most severe; chips highlighted red differ from NVD."));
  const detail = el("div", "detail");
  detail.id = "noise-detail";
  tab.appendChild(detail);
}

function showDetail(cid) {
  const c = D.cves.find(x => x.cve_id === cid);
  const detail = document.getElementById("noise-detail");
  detail.innerHTML = "";
  const card = el("div", "card");
  const h = el("div", "card-head");
  h.appendChild(el("h3", null, cid));
  h.appendChild(bandBadge(c.nvd_band, `NVD ${c.nvd_score} ${c.nvd_band}`));
  const v = el("span", "vec");
  renderVector(v, c.nvd_vector);
  h.appendChild(v);
  card.appendChild(h);
  card.appendChild(el("p", "desc", c.description));

  const ok = c.noise_runs.filter(r => r.valid);
  if (!ok.length) {
    card.appendChild(el("p", "err", "No valid runs for this CVE."));
    detail.appendChild(card);
    return;
  }
  const s = c.stats;

  card.appendChild(el("h4", null, `Vectors across ${ok.length} runs (red chips differ from NVD)`));
  for (const [vec, n, sc, bd] of s.vector_counts) {
    const row = el("div", "vec-row");
    row.appendChild(el("span", "count", `×${n}`));
    const vv = el("span", "vec");
    renderVector(vv, vec, letters(c.nvd_vector));
    row.appendChild(vv);
    row.appendChild(bandBadge(bd, String(sc)));
    card.appendChild(row);
  }

  card.appendChild(el("h4", null, "Per-metric probabilities (one stacked bar per run, mean last)"));
  const grid = el("div", "prob-grid");
  for (const m of ORDER) grid.appendChild(probBlock(m, ok, s.mean_probabilities[m]));
  card.appendChild(grid);

  card.appendChild(el("h4", null, "Run log"));
  const t = el("table", "grid small");
  const head = el("tr");
  for (const h2 of ["#", "vector", "score", "band", "latency s", "in tok", "error"]) head.appendChild(el("th", null, h2));
  t.appendChild(head);
  for (const r of c.noise_runs) {
    const tr = el("tr");
    tr.appendChild(el("td", null, String(r.repeat)));
    if (r.valid) {
      const cell = el("td");
      const vv = el("span", "vec small");
      renderVector(vv, r.vector, letters(c.nvd_vector));
      cell.appendChild(vv);
      tr.appendChild(cell);
      tr.appendChild(el("td", null, String(r.score)));
      tr.appendChild(el("td")).appendChild(bandBadge(r.band));
      tr.appendChild(el("td", null, fmt(r.latency_s, 2)));
      tr.appendChild(el("td", null, String(r.input_tokens ?? "–")));
      tr.appendChild(el("td", null, ""));
    } else {
      for (let i = 0; i < 5; i++) tr.appendChild(el("td", null, "–"));
      tr.appendChild(el("td", "err", r.error || "invalid"));
    }
    t.appendChild(tr);
  }
  card.appendChild(t);
  detail.appendChild(card);
  detail.scrollIntoView({ behavior: "smooth", block: "start" });
}

/* ---------- Variants tab ---------- */
function renderVariants() {
  const tab = document.getElementById("tab-variants");
  tab.innerHTML = "";
  const withV = D.cves.filter(c => c.variants && c.variants.length);
  tab.appendChild(el("h2", null, "Variants — reworded descriptions, same facts"));
  if (!withV.length) {
    tab.appendChild(el("p", null, "No variants defined (data/variants.jsonl is empty)."));
    return;
  }
  tab.appendChild(el("p", "hint",
    "Δ = severity-index shift vs the original's runs (Σ p·rank, 0–1, per metric). " +
    "Bold red/green = beyond the original's own run-to-run noise floor (row 1) — only those are evidence of a framing effect. " +
    "[X→Y] marks a change in the most common answer; chips shown red differ from the original's modal vector. " +
    "Click a variant row for its text and the meaning-preservation fact checklist."));

  for (const c of withV) {
    const card = el("div", "card");
    const h = el("div", "card-head");
    h.appendChild(el("h3", null, c.cve_id));
    h.appendChild(bandBadge(c.nvd_band, `NVD ${c.nvd_score} ${c.nvd_band}`));
    if (c.stats) {
      h.appendChild(el("span", "orig-note",
        `original modal ${c.stats.modal_vector.replace("CVSS:3.1/", "")} · mean ${fmt(c.stats.score_mean)} (${c.stats.score_lo}–${c.stats.score_hi})`));
    }
    card.appendChild(h);

    const t = el("table", "grid");
    const head = el("tr");
    for (const th of ["Version", "Modal vector", "Score mean (range)", "Δ score", ...ORDER.map(m => "Δ" + m)])
      head.appendChild(el("th", null, th));
    t.appendChild(head);

    if (c.stats) {
      const floor = el("tr", "floor");
      floor.appendChild(el("td", null, "noise floor"));
      floor.appendChild(el("td", null, ""));
      floor.appendChild(el("td", null, fmt(c.stats.score_hi - c.stats.score_lo, 1)));
      floor.appendChild(el("td", null, ""));
      for (const m of ORDER) floor.appendChild(el("td", null, fmt(c.stats.noise_floor[m])));
      t.appendChild(floor);
    }

    for (const v of c.variants) {
      const tr = el("tr", v.stats ? "row-click" : null);
      tr.appendChild(el("td", "kind-" + v.variant,
        `${v.variant}${v.approved === false ? " (unapproved)" : ""} — ${v.runs.length} runs${v.errors ? ", " + v.errors + " err" : ""}`));
      if (!v.stats) {
        for (let i = 0; i < 3 + ORDER.length; i++) tr.appendChild(el("td", null, "–"));
        t.appendChild(tr);
        continue;
      }
      const cell = el("td");
      const vv = el("span", "vec small");
      renderVector(vv, v.stats.modal_vector, c.stats ? letters(c.stats.modal_vector) : null);
      cell.appendChild(vv);
      tr.appendChild(cell);
      tr.appendChild(el("td", null, `${fmt(v.stats.score_mean)} (${v.stats.score_lo}–${v.stats.score_hi})`));
      tr.appendChild(el("td", v.delta_score > 0.005 ? "up" : v.delta_score < -0.005 ? "down" : null, sgn(v.delta_score)));
      for (const m of ORDER) {
        const md = v.metric_deltas[m];
        tr.appendChild(el("td",
          md.beyond ? "delta strong " + (md.delta > 0 ? "up" : "down") : "delta muted",
          sgn(md.delta) + (md.change ? ` [${md.change[0]}→${md.change[1]}]` : "")));
      }
      tr.onclick = () => toggleVariant(card, v, c);
      t.appendChild(tr);
      v._row = tr;
    }
    card.appendChild(t);
    card.appendChild(el("div", "vdetail"));
    tab.appendChild(card);
  }
}

function toggleVariant(card, v, c) {
  const vd = card.querySelector(".vdetail");
  const open = vd.dataset.open === v.variant;
  card.querySelectorAll("tr.sel").forEach(r => r.classList.remove("sel"));
  if (open) { vd.innerHTML = ""; vd.dataset.open = ""; return; }
  vd.dataset.open = v.variant;
  v._row.classList.add("sel");
  vd.innerHTML = "";
  vd.appendChild(el("h4", null, `${v.variant} text (what was sent to Jev)`));
  vd.appendChild(el("p", "desc", v.text));
  vd.appendChild(el("h4", null, "Original text"));
  vd.appendChild(el("p", "desc dim", c.description));
  if (v.facts) {
    vd.appendChild(el("h4", null, "Fact checklist (meaning preservation)"));
    const ft = el("table", "grid small facts");
    for (const [k, val] of Object.entries(v.facts)) {
      const tr = el("tr");
      tr.appendChild(el("td", "fact-key", k));
      tr.appendChild(el("td", null, val));
      ft.appendChild(tr);
    }
    vd.appendChild(ft);
  }
  if (v.runs.length) {
    vd.appendChild(el("h4", null, "Per-metric probabilities for this variant"));
    const grid = el("div", "prob-grid");
    for (const m of ORDER) grid.appendChild(probBlock(m, v.runs, v.stats.mean_probabilities[m]));
    vd.appendChild(grid);
  }
}

/* ---------- Direction tab ---------- */
function renderDirection() {
  const tab = document.getElementById("tab-direction");
  tab.innerHTML = "";
  tab.appendChild(el("h2", null, "Direction across CVEs"));
  tab.appendChild(el("p", "hint",
    "Per version and metric: CVEs whose severity index moved beyond the noise floor toward more severe (↑) or less severe (↓). " +
    "Descriptive only — the pilot is too small for significance tests."));
  const t = el("table", "grid");
  const head = el("tr");
  for (const th of ["Version", "Mean Δ score", ...ORDER]) head.appendChild(el("th", null, th));
  t.appendChild(head);
  for (const kind of KINDS) {
    const tr = el("tr");
    tr.appendChild(el("td", "kind-" + kind, kind));
    const ms = D.mean_score_shift[kind];
    tr.appendChild(el("td", ms > 0.005 ? "up" : ms < -0.005 ? "down" : null, sgn(ms)));
    for (const m of ORDER) {
      const d = D.direction[kind][m];
      const cell = el("td");
      if (d.up) cell.appendChild(el("span", "up", `${d.up}↑ `));
      if (d.down) cell.appendChild(el("span", "down", `${d.down}↓`));
      if (!d.up && !d.down) cell.textContent = "–";
      tr.appendChild(cell);
    }
    t.appendChild(tr);
  }
  tab.appendChild(t);

  const covered = D.cves.filter(c => c.variants && c.variants.some(v => v.stats)).map(c => c.cve_id);
  tab.appendChild(el("p", "hint", `CVEs with variant runs: ${covered.join(", ") || "none yet"}.`));
}

/* ---------- boot ---------- */
async function boot() {
  const res = await fetch("/api/bundle");
  if (!res.ok) {
    let msg = "HTTP " + res.status;
    try { msg = (await res.json()).error || msg; } catch { /* keep status */ }
    document.getElementById("meta-line").textContent = "Failed to load data: " + msg;
    return;
  }
  D = await res.json();
  ORDER = D.meta.metric_order || ORDER_FALLBACK;
  document.getElementById("meta-line").textContent =
    `model ${D.meta.model} · CVSS v${D.meta.cvss_version} · ${D.meta.repeats} repeats/input · ` +
    `${D.meta.total_calls} calls logged (${D.meta.noise_calls} noise, ${D.meta.variant_calls} variant, ${D.meta.other_calls} test) · ` +
    `${D.meta.input_tokens.toLocaleString()} input tokens ≈ $${D.meta.cost_usd.toFixed(4)} · data rebuilt ${D.meta.generated_at}`;
  renderNoise();
  renderVariants();
  renderDirection();
  const initial = location.hash.replace("#", "");
  if (initial) {
    const b = document.querySelector(`nav button[data-tab="${initial}"]`);
    if (b) b.click();
  }
}

document.querySelector("nav").addEventListener("click", e => {
  const b = e.target.closest("button[data-tab]");
  if (!b) return;
  document.querySelectorAll("nav button").forEach(x => x.classList.toggle("active", x === b));
  document.querySelectorAll(".tab").forEach(s => s.classList.toggle("active", s.id === "tab-" + b.dataset.tab));
  history.replaceState(null, "", "#" + b.dataset.tab);
});

boot();
