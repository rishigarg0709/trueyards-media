"""Balance watch (Rishi, 18 Nov 2026: Gemini credits ran out at 12:28 and nobody warned him).

Every 2 hours, and right after every image job, checks every paid or capped service, estimates how many days
are left, writes ops/balances.json and ops/BALANCES.md, and alerts Rishi (WhatsApp plus email, through the bot's
/smx/alert route) the moment anything goes low or runs out, again at most every 12 hours while it stays that way.
Thresholds and Gemini top-ups live in config/balances.json. Keys come from GitHub secrets only; none is printed.
"""
import datetime, json, os, re, subprocess, urllib.error, urllib.request

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
NOW = datetime.datetime.now(datetime.timezone.utc)
CFG = json.load(open("config/balances.json"))
OUT_JSON, OUT_MD = "ops/balances.json", "ops/BALANCES.md"
RANK = {"ok": 0, "check": 1, "low": 2, "out": 3}


def http(url, body=None, headers=None, method=None, timeout=30):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"), headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf8", "replace")
        try:
            return e.code, json.loads(txt)
        except Exception:
            return e.code, {"raw": txt[:300]}


def days(left, burn):
    return round(left / burn, 1) if burn and burn > 0 and left is not None else None


def grade(left, runway, warn_amount=None, warn_days=None):
    if left is not None and left <= 0:
        return "out"
    if (warn_amount is not None and left is not None and left < warn_amount) or (warn_days is not None and runway is not None and runway < warn_days):
        return "low"
    return "ok"


def ist(dt):
    return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M")


# ---------- Gemini (images) ----------
def gemini():
    c = CFG["gemini"]
    key = os.environ.get("GEMINI_API_KEY", "")
    out = {"id": "gemini", "name": "Gemini images", "unit": "INR", "link": "https://ai.studio/projects",
           "action": "Top up prepaid credits in Google AI Studio (TrueYards Autopilot project, Billing), then tell any project chat the amount so the estimate resets"}
    probe = None
    if key:
        for model in c.get("probe_models", []):
            code, j = http(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                           {"contents": [{"parts": [{"text": "ok"}]}], "generationConfig": {"maxOutputTokens": 1}}, {"x-goog-api-key": key})
            if code == 404:
                continue
            probe = code
            break
    # Spend since the last recorded top-up (ops/gemini_spend.jsonl is written by scripts/cloud_media.py).
    spend = []
    if os.path.exists("ops/gemini_spend.jsonl"):
        for line in open("ops/gemini_spend.jsonl"):
            try:
                spend.append(json.loads(line))
            except Exception:
                pass
    prices = c.get("inr_per_image_by_model", {})
    def rate(s):  # per-model price; batch is half (Rishi, 18 Nov: Pro for hook and cover, 3.1 Flash for the rest)
        full = prices.get(s.get("model") or "", c["inr_per_image"])
        return full / 2 if s.get("mode") == "batch" else full
    week_ago = (NOW - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%MZ")
    burn = sum(s["n"] * rate(s) for s in spend if s["at"] >= week_ago) / 7
    burn = max(burn, c.get("planned_daily_inr", 0))  # the spend log is young; plan on the expected daily spend
    tops = sorted(c.get("topups", []), key=lambda t: t["at"])
    left = None
    if tops:
        last = tops[-1]
        used = sum(s["n"] * rate(s) for s in spend if s["at"] >= last["at"])
        left = round(last["inr"] - used)
    runway = days(left, burn)
    if probe == 402:
        status, detail = "out", "Google refuses every image: prepaid credits are depleted (HTTP 402)"
        left = 0 if left is None or left > 0 else left
    elif probe == 429:
        status, detail = "low", "Google is rate limiting or quota capped (HTTP 429)"
    elif probe and probe >= 400:
        status, detail = "check", f"Test call answered HTTP {probe}"
    else:
        status = grade(left, runway, c.get("warn_inr"), c.get("warn_days")) if left is not None else ("ok" if probe == 200 else "check")
        if left is not None:
            detail = f"About INR {left} left of the INR {tops[-1]['inr']} top-up on {tops[-1]['at'][:10]}"
        elif probe == 200:
            detail = "Working. Credit left is unknown until a top-up amount is recorded in config/balances.json"
        else:
            detail = "Could not run the test call"
    # Daily image budget: a runaway job should not drain the credit unnoticed.
    today = NOW.astimezone(IST).strftime("%Y-%m-%d")
    spent_today = sum(s["n"] * rate(s) for s in spend
                      if datetime.datetime.strptime(s["at"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=datetime.timezone.utc).astimezone(IST).strftime("%Y-%m-%d") == today)
    cap = c.get("daily_warn_inr")
    if cap and spent_today > cap and status == "ok":
        status, detail = "low", f"Spent about INR {round(spent_today)} on images today, above the INR {cap} daily budget. " + detail
    out.update(status=status, left=left, burn_per_day=round(burn), runway_days=runway, detail=detail, spent_today=round(spent_today))
    return out


# ---------- Meta ad account (FIT ads, Jind ads, TrueYards boost: one prepaid account) ----------
def meta():
    c = CFG["meta"]
    tok = os.environ.get("META_TOKEN", "")
    acct = json.load(open("config/meta.json"))["ad_account_id"]
    out = {"id": "meta", "name": "Meta ad account (prepaid)", "unit": "INR", "link": f"https://business.facebook.com/billing_hub/accounts/details?asset_id={acct.replace('act_', '')}",
           "action": "Add prepaid funds in Meta Billing for the TrueYards ad account (FIT ads, Jind ads and the TrueYards boost all draw on it)"}
    if not tok:
        out.update(status="check", left=None, burn_per_day=None, runway_days=None, detail="META_TOKEN not available")
        return out
    G = "https://graph.facebook.com/v23.0"
    code, a = http(f"{G}/{acct}?fields=account_status,currency,amount_spent,spend_cap,balance,funding_source_details&access_token={tok}")
    if code != 200:
        out.update(status="check", left=None, burn_per_day=None, runway_days=None, detail=f"Meta answered HTTP {code}")
        return out
    code, ins = http(f"{G}/{acct}/insights?date_preset=last_7d&fields=spend&access_token={tok}")
    spent7 = float(((ins.get("data") or [{}])[0]).get("spend") or 0) if code == 200 else 0.0
    burn = spent7 / 7
    cap, used = int(a.get("spend_cap") or 0), int(a.get("amount_spent") or 0)
    left = round((cap - used) / 100) if cap else None
    shown = ((a.get("funding_source_details") or {}).get("display_string") or "")
    m = re.search(r"([\d,]+(?:\.\d+)?)", shown) if "balance" in shown.lower() else None
    if m:
        left = round(float(m.group(1).replace(",", "")))
    # FIT ads are ramping (Rishi, 18 Nov): plan on today's planned daily spend, not last week's.
    burn = max(burn, c.get("planned_daily_inr", 0))
    runway = days(left, burn)
    status = "out" if a.get("account_status") not in (1, None) else grade(left, runway, c.get("warn_inr"), c.get("warn_days"))
    detail = f"About INR {left} left, spending about INR {round(burn)} a day" if left is not None else "Balance not reported by Meta"
    if a.get("account_status") not in (1, None):
        detail = f"Ad account status {a.get('account_status')} (not active)"
    out.update(status=status, left=left, burn_per_day=round(burn), runway_days=runway, detail=detail)
    return out


# ---------- ElevenLabs (voice and music) ----------
def elevenlabs():
    c = CFG["elevenlabs"]
    k = os.environ.get("ELEVENLABS_API_KEY", "")
    out = {"id": "elevenlabs", "name": "ElevenLabs voice and music", "unit": "credits", "link": "https://elevenlabs.io/app/subscription",
           "action": "Buy extra credits or upgrade the ElevenLabs plan, or wait for the monthly reset"}
    code, j = http("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": k}) if k else (0, {})
    if code != 200:
        out.update(status="check", left=None, burn_per_day=None, runway_days=None, detail=f"ElevenLabs answered HTTP {code}")
        return out
    left = int(j.get("character_limit", 0)) - int(j.get("character_count", 0))
    reset = j.get("next_character_count_reset_unix")
    reset_s = ist(datetime.datetime.fromtimestamp(reset, datetime.timezone.utc)) if reset else "unknown"
    burn = c.get("credits_per_day", 0)
    runway = days(left, burn)
    status = grade(left, runway, c.get("warn_credits"), None)
    if reset and runway is not None and runway * 86400 + NOW.timestamp() > reset:
        status = "ok" if status == "low" and left > 0 else status  # resets before it runs out
    out.update(status=status, left=left, burn_per_day=burn, runway_days=runway, detail=f"{left:,} credits left, resets {reset_s} IST")
    return out


# ---------- Apify (trend scan) ----------
def apify():
    c = CFG["apify"]
    t = os.environ.get("APIFY_TOKEN", "")
    out = {"id": "apify", "name": "Apify (trend scan)", "unit": "USD", "link": "https://console.apify.com/billing",
           "action": "Upgrade the Apify plan or skip the comment mining in the weekly scan until the month resets"}
    code, j = http("https://api.apify.com/v2/users/me/limits", headers={"Authorization": f"Bearer {t}"}) if t else (0, {})
    if code != 200:
        out.update(status="check", left=None, burn_per_day=None, runway_days=None, detail=f"Apify answered HTTP {code}")
        return out
    d = j.get("data", {})
    used = float((d.get("current") or {}).get("monthlyUsageUsd") or 0)
    cap = float((d.get("limits") or {}).get("maxMonthlyUsageUsd") or 0)
    left = round(cap - used, 2) if cap else None
    status = "out" if left is not None and left <= 0 else "low" if cap and used / cap >= c.get("warn_share", 0.8) else "ok"
    out.update(status=status, left=left, burn_per_day=None, runway_days=None, detail=f"USD {used:.2f} used of USD {cap:.2f} this month")
    return out


# ---------- Cloudflare Workers AI (free backup images) ----------
def cloudflare():
    out = {"id": "cloudflare", "name": "Cloudflare free images (backup)", "unit": "neurons per day", "link": "https://dash.cloudflare.com",
           "action": "Nothing to pay: it resets at 05:30 IST. Upgrade to Workers Paid only if the backup is needed every day"}
    p = "library/gen/_last_run.txt"
    txt = open(p).read() if os.path.exists(p) else ""
    hit = "daily free allocation" in txt
    # The log has no date of its own: use the time it was last committed. The allowance resets at 00:00 UTC (05:30 IST).
    try:
        when = subprocess.run(["git", "log", "-1", "--format=%cI", "--", p], capture_output=True, text=True, timeout=20).stdout.strip()
        last = datetime.datetime.fromisoformat(when) if when else None
    except Exception:
        last = None
    status = "out" if hit and last and last.astimezone(datetime.timezone.utc).date() == NOW.date() else "ok"
    detail = "Today's free allowance is used up; resets 05:30 IST" if status == "out" else "Free allowance available"
    out.update(status=status, left=None, burn_per_day=None, runway_days=None, detail=detail)
    return out


# ---------- WhatsApp wallet (bot estimate) ----------
def whatsapp():
    c = CFG["whatsapp"]
    url, key = os.environ.get("PERF_URL", ""), os.environ.get("PERF_KEY", "")
    out = {"id": "whatsapp", "name": "WhatsApp wallet (autopilot, broadcasts, alerts)", "unit": "INR", "link": "https://business.facebook.com/billing_hub/accounts/details?asset_id=1088176977434603",
           "action": "Top up the WhatsApp wallet in Meta Billing, then enter the new balance in the inbox app (Funds box)"}
    code, j = http(f"{url}?days=7", headers={"x-perf-key": key}) if url and key else (0, {})
    if code != 200:
        out.update(status="check", left=None, burn_per_day=None, runway_days=None, detail=f"Bot answered HTTP {code}")
        return out
    wa = j.get("wa", {})
    left, burn = wa.get("fundsLeft"), float(wa.get("budgetInr") or c.get("daily_inr", 1000))
    runway = days(left, burn)
    if wa.get("hold"):
        status, detail = "out", "Meta is refusing sends (empty wallet hold); autopilot paused"
    elif left is None:
        status, detail = "check", "No balance entered in the inbox app, so the estimate is unknown"
    elif left < 0:
        status, detail = "check", f"Estimate is INR {left}, below zero while sends still go through: enter the real balance in the inbox app"
    else:
        status, detail = grade(left, runway, c.get("warn_inr"), c.get("warn_days")), f"About INR {left} left at INR {round(burn)} a day"
    out.update(status=status, left=left, burn_per_day=round(burn), runway_days=runway, detail=detail)
    return out


def alert(checks, prev):
    """WhatsApp plus email to Rishi through the bot, for anything that turned low or out (again every N hours)."""
    url, key = os.environ.get("PERF_URL", ""), os.environ.get("PERF_KEY", "")
    sent = dict(prev.get("alerted", {}))
    every = datetime.timedelta(hours=CFG.get("alert_every_hours", 12))
    old = {c["id"]: c.get("status") for c in prev.get("checks", [])}
    due = []
    gem_out = any(c["id"] == "gemini" and c["status"] == "out" for c in checks)
    for c in checks:
        # The free Cloudflare backup resets every morning: only worth a message when Gemini is down too (no image source left).
        if c["id"] == "cloudflare" and not gem_out:
            sent.pop(c["id"], None)
            continue
        if c["status"] not in ("low", "out"):
            sent.pop(c["id"], None)
            continue
        last = sent.get(c["id"])
        worse = RANK[c["status"]] > RANK.get(old.get(c["id"], "ok"), 0)
        if worse or not last or NOW - datetime.datetime.fromisoformat(last) >= every:
            due.append(c)
    if not due or not url or not key:
        return sent, []
    base = url.split("/perf/summary")[0]
    lines = [f"{'OUT' if c['status'] == 'out' else 'LOW'}: {c['name']}. {c['detail']}" + (f" About {c['runway_days']} days left." if c.get("runway_days") is not None and c["status"] == "low" else "") + f" Fix: {c['action']}." for c in due]
    subject = "Top up needed: " + ", ".join(c["name"].split(" (")[0] for c in due)
    code, _ = http(f"{base}/smx/alert", {"subject": subject, "text": "\n".join(lines)}, {"x-smx-key": key})
    if code == 200:
        for c in due:
            sent[c["id"]] = NOW.isoformat()
    return sent, [c["id"] for c in due] if code == 200 else []


def _age_min(prev):
    try:
        t = datetime.datetime.strptime(prev["checked_at"], "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        return (NOW - t).total_seconds() / 60
    except Exception:
        return 1e9


def main():
    prev = json.load(open(OUT_JSON)) if os.path.exists(OUT_JSON) else {}
    # GitHub's own schedule proved unreliable (18 Nov review: no scheduled run fired in 8 hours), so this job is also
    # started after every meta-ops, social-ops and ads-ops run. Those "soft" starts skip when the last check is fresh.
    if os.environ.get("SOFT") == "1" and _age_min(prev) < 90:
        open("ops/.unchanged", "w").write("1"); print("fresh, skipped"); return
    checks = []
    for f in (gemini, meta, whatsapp, elevenlabs, apify, cloudflare):
        try:
            checks.append(f())
        except Exception as e:  # one broken check never stops the others
            checks.append({"id": f.__name__, "name": f.__name__, "status": "check", "left": None, "burn_per_day": None, "runway_days": None, "detail": f"check failed: {type(e).__name__}", "action": "", "link": ""})
    alerted, now_sent = alert(checks, prev)
    os.makedirs("ops", exist_ok=True)
    body = {"checked_at": ist(NOW), "checks": checks, "alerted": alerted}
    same = {k: v for k, v in prev.items() if k != "checked_at"} == {k: v for k, v in body.items() if k != "checked_at"}
    json.dump(body, open(OUT_JSON, "w"), indent=1, ensure_ascii=False)
    icon = {"ok": "OK", "check": "Check", "low": "LOW", "out": "OUT"}
    md = [f"# Balances (checked {body['checked_at']} IST; runs about every 2 hours and after every image job)", "", "| Service | Status | Left | Per day | Days left | Detail | Fix |", "|---|---|---|---|---|---|---|"]
    for c in sorted(checks, key=lambda c: -RANK.get(c["status"], 0)):
        left = "" if c.get("left") is None else f"{c['left']:,} {c['unit']}"
        md.append(f"| {c['name']} | {icon.get(c['status'], c['status'])} | {left} | {c.get('burn_per_day') or ''} | {c.get('runway_days') if c.get('runway_days') is not None else ''} | {c['detail']} | {c['action']} |")
    md += ["", "X API prepaid credit has no balance API: check developer.x.com when posts start failing.", "Thresholds and Gemini top-ups: config/balances.json."]
    open(OUT_MD, "w").write("\n".join(md) + "\n")
    print(json.dumps({"same_as_before": same, "alerted": now_sent, "status": {c["id"]: c["status"] for c in checks}}))
    if same and _age_min(prev) < 180:  # still commit a heartbeat every 3 hours so a stopped watch is visible
        open("ops/.unchanged", "w").write("1")


if __name__ == "__main__":
    main()
