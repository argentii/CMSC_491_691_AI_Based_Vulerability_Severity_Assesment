"""Read-only web dashboard for the pilot data. Python stdlib only — no new dependencies.

Serves a single-page viewer (pilot/web/) plus a JSON bundle built from data/*.jsonl.
Makes NO Jev calls and never reads .env; everything shown comes from saved runs.

Usage: python web.py            # http://127.0.0.1:8034
       python web.py --port 9000 --host 0.0.0.0   (bind wider than localhost: anyone on
       the network can read the data; only do this deliberately)
"""
import argparse
import json
import sys
import time
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
from parse import ORDER  # noqa: E402
from score import score  # noqa: E402

WEB = Path(__file__).resolve().parent / "web"
KINDS = ["neutral", "alarmist", "downplaying"]
# Least -> most severe option letters per metric, for the 0..1 severity index (see summarize.py).
SEV = {"AV": "PLAN", "AC": "HL", "PR": "HLN", "UI": "RN", "S": "UC", "C": "NLH", "I": "NLH", "A": "NLH"}
MIN_FLOOR = 0.05  # same noise floor as summarize.py


def load(path):
    return [json.loads(l) for l in open(path) if l.strip()] if path.exists() else []


def ok_runs(rs):
    return [r for r in rs if r.get("ok") and (r.get("parsed") or {}).get("valid")]


def letters(vector):
    return dict(p.split(":") for p in vector.split("/")[1:])


def trim_run(r):
    """Keep only what the UI needs; raw/request stay out of the JSON bundle."""
    p = r.get("parsed") or {}
    out = {
        "timestamp": r.get("timestamp"), "latency_s": r.get("latency_s"),
        "request_id": r.get("request_id"), "model_version": r.get("model_version"),
        "repeat": r.get("repeat"), "ok": r.get("ok"), "valid": p.get("valid"),
        "error": p.get("error") or (None if r.get("ok") else "api error"),
        "input_tokens": (r.get("usage") or {}).get("input_tokens"),
    }
    if p.get("valid"):
        s, b = score(p["vector"])
        out.update(vector=p["vector"], metrics=p["metrics"], probabilities=p["probabilities"],
                   score=s, band=b)
    return out


def sev_values(rs, m):
    k = len(SEV[m]) - 1
    return [sum(r["parsed"]["probabilities"][m].get(o, 0) * i / k for i, o in enumerate(SEV[m])) for r in rs]


def sev_index(rs, m):
    return sum(sev_values(rs, m)) / len(rs)


def sev_noise(rs, m):
    vals = sev_values(rs, m)
    return max(max(vals) - min(vals), MIN_FLOOR)


def group_stats(rs):
    """Aggregate a set of ok runs for one (cve, version) group."""
    vectors = Counter(r["parsed"]["vector"] for r in rs)
    modal = vectors.most_common(1)[0][0]
    scored = [score(r["parsed"]["vector"]) for r in rs]
    scores = [s for s, _ in scored]
    mean_p = {m: {o: sum(r["parsed"]["probabilities"][m].get(o, 0) for r in rs) / len(rs)
                  for o in SEV[m]} for m in ORDER}
    agreement = {}
    for m in ORDER:
        cnt = Counter(r["parsed"]["metrics"][m] for r in rs)
        agreement[m] = cnt.most_common(1)[0][1] / len(rs)
    spread = 0.0
    for m in ORDER:
        for o in mean_p[m]:
            vals = [r["parsed"]["probabilities"][m].get(o, 0) for r in rs]
            spread = max(spread, max(vals) - min(vals))
    return {
        "n": len(rs), "modal_vector": modal, "distinct_vectors": len(vectors),
        "vector_counts": [[v, n, *score(v)] for v, n in sorted(vectors.items(), key=lambda kv: -kv[1])],
        "score_mean": sum(scores) / len(scores), "score_lo": min(scores), "score_hi": max(scores),
        "bands": sorted({b for _, b in scored}),
        "mean_probabilities": mean_p, "agreement": agreement, "max_prob_spread": spread,
        "noise_floor": {m: sev_noise(rs, m) for m in ORDER},
    }


def build_bundle():
    cves = load(config.CVES_PATH)
    runs = load(config.RUNS_PATH)
    vdefs = load(config.VARIANTS_PATH)
    noise = [r for r in runs if r.get("run_type") == "noise"]
    vruns = [r for r in runs if r.get("run_type") == "variant"]
    total_tokens = sum((r.get("usage") or {}).get("input_tokens") or 0 for r in runs)

    out = {"meta": {
        "model": config.JEV_MODEL, "cvss_version": config.CVSS_VERSION, "repeats": config.REPEATS,
        "total_calls": len(runs), "noise_calls": len(noise), "variant_calls": len(vruns),
        "other_calls": len(runs) - len(noise) - len(vruns),
        "input_tokens": total_tokens, "cost_usd": total_tokens * 0.042 / 1e6,
        "generated_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "metric_order": ORDER,
    }}

    direction = {k: {m: {"up": 0, "down": 0} for m in ORDER} for k in KINDS}
    score_shift = {k: [] for k in KINDS}

    cards = []
    for c in cves:
        cid = c["cve_id"]
        rs = [r for r in noise if r.get("cve_id") == cid]
        ok = ok_runs(rs)
        card = {k: c[k] for k in c if k != "description"}
        card["description"] = c["description"]
        card["noise_runs"] = [trim_run(r) for r in sorted(rs, key=lambda r: r.get("repeat") or 0)]
        card["errors"] = len(rs) - len(ok)
        card["stats"] = None
        card["nvd_match"] = None
        if ok:
            st = group_stats(ok)
            card["stats"] = st
            nvd = letters(c["nvd_vector"])
            jev = letters(st["modal_vector"])
            match = [m for m in ORDER if nvd[m] == jev[m]]
            card["nvd_match"] = {"metrics": match, "n": len(match), "of": len(ORDER),
                                 "diff": [m for m in ORDER if m not in match]}
        # variants
        vlist = []
        vdefs_cve = [v for v in vdefs if v["cve_id"] == cid]
        for vdef in vdefs_cve:
            vr = ok_runs([r for r in vruns if r.get("cve_id") == cid and r.get("variant") == vdef["variant"]])
            item = {"variant": vdef["variant"], "text": vdef["text"], "facts": vdef.get("facts"),
                    "approved": vdef.get("approved"), "runs": [trim_run(r) for r in vr],
                    "errors": len([r for r in vruns if r.get("cve_id") == cid and r.get("variant") == vdef["variant"]]) - len(vr)}
            if ok and vr:
                vs = group_stats(vr)
                item["stats"] = vs
                o_scores = [score(r["parsed"]["vector"])[0] for r in ok]
                o_letters = letters(group_stats(ok)["modal_vector"])
                v_letters = letters(vs["modal_vector"])
                d_score = vs["score_mean"] - sum(o_scores) / len(o_scores)
                item["delta_score"] = d_score
                item["metric_deltas"] = {}
                score_shift[vdef["variant"]].append(d_score)
                for m in ORDER:
                    d = sev_index(vr, m) - sev_index(ok, m)
                    beyond = abs(d) > sev_noise(ok, m)
                    item["metric_deltas"][m] = {"delta": d, "beyond": beyond,
                                                "change": None if v_letters[m] == o_letters[m] else [o_letters[m], v_letters[m]]}
                    if beyond:
                        direction[vdef["variant"]][m]["up" if d > 0 else "down"] += 1
            vlist.append(item)
        # keep canonical order neutral/alarmist/downplaying
        card["variants"] = sorted(vlist, key=lambda v: KINDS.index(v["variant"]) if v["variant"] in KINDS else 99)
        cards.append(card)

    out["direction"] = {k: {m: direction[k][m] for m in ORDER} for k in KINDS}
    out["mean_score_shift"] = {k: (sum(score_shift[k]) / len(score_shift[k]) if score_shift[k] else None)
                               for k in KINDS}
    out["cves"] = cards
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quiet
        pass

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._serve_file(WEB / "index.html", "text/html; charset=utf-8")
        elif path == "/app.js":
            self._serve_file(WEB / "app.js", "text/javascript; charset=utf-8")
        elif path == "/style.css":
            self._serve_file(WEB / "style.css", "text/css; charset=utf-8")
        elif path == "/api/bundle":
            try:
                body = json.dumps(build_bundle()).encode()
            except Exception as e:  # surface data problems in the UI instead of a stack trace page
                body = json.dumps({"error": f"{type(e).__name__}: {e}"}).encode()
                self._send(500, "application/json", body)
                return
            self._send(200, "application/json", body)
        elif path == "/report.md":
            self._serve_file(config.REPORT_PATH, "text/markdown; charset=utf-8")
        else:
            self._send(404, "text/plain", b"not found")

    def _serve_file(self, p, ctype):
        if not p.exists():
            self._send(404, "text/plain", b"missing: " + p.name.encode())
            return
        self._send(200, ctype, p.read_bytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8034)
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"pilot dashboard on http://{a.host}:{a.port}  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
