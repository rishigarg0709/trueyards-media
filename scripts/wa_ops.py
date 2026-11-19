#!/usr/bin/env python3
"""Cloud route to the WhatsApp bot for agents (Rishi, 19 Nov 2026: everything runs in the cloud; no agent changes
WhatsApp campaigns through a browser on his laptop).

Two ways to use it, both in the cloud:
  1. Push a request file wa/requests/<name>.json; the answer is written to wa/results/<name>.json.
       {"by": "Paid Media Buyer", "op": "switches"}
       {"by": "Paid Media Buyer", "ops": [{"op": "broadcast.create", "args": {...}}, {"op": "broadcasts", "args": {"days": 1}}]}
  2. Start the workflow wa-ops by hand with inputs op, args (JSON) and by; the answer is printed in the run log.
     An empty op lists every action.

The bot (POST /smx/ops, src/ops.mjs in the bot repo) decides what is allowed. It answers with counts and settings only.
This repo and its run logs are PUBLIC: never put a phone number or a person's name in a request file. A request that
holds a phone number is refused here, and every answer is masked once more before it is written or printed.
A new broadcast created here is held until Rishi replies GO on WhatsApp (Directive D4).
"""
import datetime, glob, json, os, re, sys, urllib.error, urllib.request

BASE = os.environ.get("PERF_URL", "").split("/perf/")[0].rstrip("/")
KEY = os.environ.get("PERF_KEY", "")
PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)")
META_ID = re.compile(r"(?<!\d)\d{15,17}(?!\d)")  # Meta account, app and template ids: not secret, but no reason to publish them
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def now():
    return datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M")


def mask(v):
    if isinstance(v, str):
        return META_ID.sub("[id]", PHONE.sub("[number]", v))
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return "[number]" if PHONE.fullmatch(str(v)) else v
    if isinstance(v, list):
        return [mask(x) for x in v]
    if isinstance(v, dict):
        return {mask(str(k)): mask(x) for k, x in v.items()}
    return None


def http(method, body=None):
    if not BASE or not KEY:
        return {"ok": False, "error": "PERF_URL or PERF_KEY is not set in this repo's secrets"}
    req = urllib.request.Request(BASE + "/smx/ops", method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"x-smx-key": KEY, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=110) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            out = json.loads(raw)
        except Exception:
            out = {"error": raw[:200]}
        out.setdefault("ok", False)
        out["http"] = e.code
        if e.code == 404:
            out["error"] = "The bot does not have the cloud route yet (bot PR #27 not deployed)"
        return out
    except Exception as e:
        return {"ok": False, "error": ("%s: %s" % (type(e).__name__, e))[:200]}


def run_one(op, by, args):
    if PHONE.search(json.dumps(args or {})):
        return {"ok": False, "op": op, "error": "A phone number is not allowed here: this repo is public. Use an audience tag"}
    return mask(http("POST", {"op": op, "by": by, "args": args or {}}))


def run_request(req):
    by = str(req.get("by") or "").strip()
    steps = req.get("ops") if isinstance(req.get("ops"), list) else [{"op": req.get("op"), "args": req.get("args")}]
    out = {"at": now(), "by": by, "results": []}
    if not by:
        out["results"].append({"ok": False, "error": '"by" is required: your role'})
        return out
    for i, s in enumerate(steps[:20]):
        r = run_one(str((s or {}).get("op") or ""), by, (s or {}).get("args") or {})
        out["results"].append(r)
        if not r.get("ok"):
            if i + 1 < len(steps):
                out["stopped"] = "Step %d failed, the remaining %d were not run" % (i + 1, len(steps) - i - 1)
            break
    return out


def main():
    if os.environ.get("MODE") == "dispatch":
        op = (os.environ.get("OP") or "").strip()
        if not op:
            cat = mask(http("GET"))
            for o in cat.get("ops", []):
                print(("CHANGE " if o.get("changes") else "LOOK   ") + o.get("op", "").ljust(22) + o.get("about", ""))
            for row in cat.get("log", [])[:20]:
                print("LOG", json.dumps(row, ensure_ascii=False))
            if not cat.get("ops"):
                print("RESULT", json.dumps(cat, ensure_ascii=False))
                sys.exit(1)
            return
        try:
            args = json.loads(os.environ.get("ARGS") or "{}")
        except Exception:
            print('RESULT {"ok": false, "error": "args is not valid JSON"}')
            sys.exit(1)
        r = run_request({"by": os.environ.get("BY") or "", "op": op, "args": args})
        print("RESULT", json.dumps(r, ensure_ascii=False, indent=1))
        sys.exit(0 if all(x.get("ok") for x in r["results"]) else 1)
    done = 0
    os.makedirs("wa/results", exist_ok=True)
    for path in sorted(glob.glob("wa/requests/*.json")):
        res = os.path.join("wa/results", os.path.basename(path))
        if os.path.exists(res):
            continue
        try:
            req = json.load(open(path))
            out = run_request(req if isinstance(req, dict) else {})
        except Exception as e:
            out = {"at": now(), "results": [{"ok": False, "error": "Request file is not valid JSON: %s" % str(e)[:120]}]}
        json.dump(out, open(res, "w"), ensure_ascii=False, indent=1)
        done += 1
        print("REQUEST", os.path.basename(path), "|", " ".join("%s:%s" % (r.get("op", "?"), "ok" if r.get("ok") else "FAILED") for r in out["results"]), "|", out.get("stopped", ""))
    print("processed", done)


if __name__ == "__main__":
    main()
