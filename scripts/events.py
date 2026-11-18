"""System event feed for SMX HQ (Rishi, 18 Nov 2026: "ensure everyone reports everything and it is reflected in the dashboard").

Agents report their own runs, but this does not depend on them. Every 15 minutes it records what actually changed:
  1. Meta: every campaign and ad set in the shared ad account (new, status change, budget change), whoever made it
     (an agent, a workflow or someone in Ads Manager).
  2. This repo: every meaningful commit (ads, reels, plans, configs, scripts), skipping routine result and fetch commits.
  3. Failures: every failed workflow run in this repo, which also alerts Rishi by WhatsApp and email.
Writes ops/events.jsonl (newest last, last 600 kept). The Control Room sync (SmxMirror.gs) copies new lines into the
Activity tab, skipping anything an agent already reported. Bot campaigns (WhatsApp broadcasts and autopilot runs) are
read by that sync straight from the bot's /smx/campaigns route. META_TOKEN comes from GitHub secrets; it is never printed.
"""
import datetime, json, os, re, subprocess, urllib.error, urllib.request

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
NOW = datetime.datetime.now(datetime.timezone.utc)
FEED, STATE = "ops/events.jsonl", "ops/events_state.json"
KEEP = 600
REPO = "https://github.com/rishigarg0709/trueyards-media"

# Commits that are routine machine output: the agent that caused them already shows up another way.
SKIP = re.compile(r"^(events|balances)$|results$|^comments?:? fetch|^comment fetch|fetch requests|run requests|^fetch[: ]|^Fetch stock photos|^Check boost status|^Verify boost|^boost_status|^jobs: |^cloud-media|^batch-poll|^merge ", re.I)
# Commit message or changed path -> (agent_id, agent name in the Agents tab)
AGENTS = [
    (r"^cos|cos/|balance watch|^balances", ("cos", "Chief of Staff")),
    (r"^ads: |^ads/|config/ads", ("pf.ads", "FIT Meta ads agent")),
    (r"learning run|^learn", ("bo.learn", "Analytics and learning")),
    (r"boost", ("pf.boost", "Boost manager")),
    (r"^perf|perf/", ("pf.plan", "Budget planner")),
    (r"carousel", ("bo.car", "Carousel")),
    (r"music", ("bo.music", "Music-only reel")),
    (r"evening", ("bo.reel2", "Evening reel")),
    (r"midday|^reel|^meta: publish|^story|^log \+ queue", ("bo.reel1", "Midday reel")),
    (r"^plan|plans/|nightly", ("bo.plan", "Nightly planner")),
    (r"news", ("mi.news", "News desk")),
    (r"trend|competitor|scans/", ("mi.trend", "Trend and competitor scan")),
    (r"comment", ("bo.comments", "Comment replies")),
    (r"learn|analytics|playbook", ("bo.learn", "Analytics and learning")),
    (r"look|style|hook|creative|image|voice|render", ("cs.looks", "Look and voice system")),
]


def ist(dt):
    return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M")


def agent_for(msg, paths):
    for pat, who in AGENTS:  # the commit message decides first, changed paths only when the message says nothing
        if re.search(pat, msg, re.I):
            return who
    for pat, who in AGENTS:
        if re.search(pat, " ".join(paths), re.I):
            return who
    return ("cos", "Chief of Staff")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def commit_events(state):
    last = state.get("last_sha")
    rng = f"{last}..HEAD" if last and git("cat-file", "-t", last).strip() == "commit" else "--since=6 hours ago"
    raw = git("log", "--reverse", "--no-merges", "--pretty=%x1e%H%x1f%ct%x1f%s", "--name-only", rng)
    out = []
    for block in raw.split("\x1e")[1:]:
        head, *files = block.strip().split("\n")
        sha, ts, msg = head.split("\x1f", 2)
        files = [f for f in files if f.strip()]
        if SKIP.search(msg.strip()) or all(f.startswith(("ops/", "library/gen/_last", "social/stats")) for f in files or ["ops/"]):
            continue
        aid, name = agent_for(msg, files)
        when = datetime.datetime.fromtimestamp(int(ts), datetime.timezone.utc)
        out.append({"id": "git:" + sha[:10], "time": ist(when), "agent_id": aid, "agent": name, "event": "changed",
                    "detail": msg[:220], "link": f"{REPO}/commit/{sha[:10]}", "source": "repo"})
    head = git("rev-parse", "HEAD").strip()
    if head:
        state["last_sha"] = head
    return out


def graph(path, tok):
    url = f"https://graph.facebook.com/v23.0/{path}{'&' if '?' in path else '?'}access_token={tok}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code}


def inr(x):
    return f"INR {int(x) // 100:,}" if x not in (None, "", "0") else ""


def meta_events(state):
    tok = os.environ.get("META_TOKEN", "")
    if not tok:
        return []
    acct = json.load(open("config/meta.json"))["ad_account_id"]
    old = state.get("meta") or {}
    first = not old
    now = {}
    out = []
    for kind, fields in (("campaign", "name,effective_status,daily_budget,lifetime_budget,objective"), ("adset", "name,effective_status,daily_budget,lifetime_budget,campaign{name}")):
        j = graph(f"{acct}/{kind}s?fields={fields}&limit=200&effective_status=[\"ACTIVE\",\"PAUSED\",\"CAMPAIGN_PAUSED\",\"ADSET_PAUSED\",\"IN_PROCESS\",\"WITH_ISSUES\",\"DISAPPROVED\",\"PENDING_REVIEW\"]", tok)
        if "error" in j:
            return []
        for x in j.get("data", []):
            key = f"{kind}:{x['id']}"
            cur = {"name": x.get("name", ""), "status": x.get("effective_status", ""), "budget": x.get("daily_budget") or x.get("lifetime_budget") or "",
                   "camp": (x.get("campaign") or {}).get("name", "")}
            now[key] = cur
            if first:
                continue
            was = old.get(key)
            label = f"Meta {kind} '{cur['name']}'" + (f" in '{cur['camp']}'" if cur["camp"] else "")
            who = ("pf.boost", "Boost manager") if "boost" in (cur["name"] + cur["camp"]).lower() else ("pf.ads", "FIT Meta ads agent")
            ev = detail = None
            if not was:
                ev, detail = "created", f"{label} created, {cur['status'].lower().replace('_', ' ')}" + (f", {inr(cur['budget'])} a day" if cur["budget"] else "")
            elif was["status"] != cur["status"]:
                st = cur["status"].lower().replace("_", " ")
                ev = "launched" if cur["status"] == "ACTIVE" else "paused" if "PAUSED" in cur["status"] else "status"
                detail = f"{label} is now {st} (was {was['status'].lower().replace('_', ' ')})"
            elif was["budget"] != cur["budget"] and cur["budget"]:
                ev, detail = "budget", f"{label} budget {inr(was['budget']) or 'none'} to {inr(cur['budget'])}"
            if ev:
                out.append({"id": f"meta:{x['id']}:{ev}:{NOW.strftime('%Y%m%d%H%M')}", "time": ist(NOW), "agent_id": who[0], "agent": who[1], "event": ev,
                            "detail": detail + " (seen in Meta)", "link": "https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=" + acct.replace("act_", ""), "source": "meta"})
    state["meta"] = now
    return out


# ---------- Failed workflow runs (automatic bug detection, 18 Nov review) ----------
RUN_OWNER = {"meta-ops": ("bo.reel.publish", "Publisher and cross-poster"), "social-ops": ("bo.reel.publish", "Publisher and cross-poster"),
             "ads-ops": ("pf.ads", "FIT Meta ads agent"), "cloud-media": ("cs.img", "Image generator"), "batch-poll": ("cs.img", "Image generator"),
             "generate-images": ("cs.img", "Image generator"), "fetch-images": ("cs.img", "Image generator")}


def ci_events():
    """Every failed GitHub workflow run of the last 6 hours becomes an event (and so an Activity row in SMX HQ)."""
    tok = os.environ.get("GH_TOKEN", "")
    req = urllib.request.Request("https://api.github.com/repos/rishigarg0709/trueyards-media/actions/runs?status=failure&per_page=20",
                                 headers={"Accept": "application/vnd.github+json", **({"Authorization": "Bearer " + tok} if tok else {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            runs = json.loads(r.read()).get("workflow_runs", [])
    except Exception:
        return []
    out = []
    for run in runs:
        when = datetime.datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        if (NOW - when).total_seconds() > 6 * 3600:
            continue
        aid, name = RUN_OWNER.get(run["name"], ("cos", "Chief of Staff"))
        msg = ((run.get("head_commit") or {}).get("message") or "").split("\n")[0][:120]
        out.append({"id": f"run:{run['id']}", "time": ist(when), "agent_id": aid, "agent": name, "event": "failed",
                    "detail": f"Workflow {run['name']} failed" + (f" on: {msg}" if msg else "") + " (seen in GitHub)", "link": run["html_url"], "source": "ci"})
    return out


def alert_failures(evs):
    """One WhatsApp and email to Rishi for new failures, through the bot (shares its 8-a-day limit)."""
    url, key = os.environ.get("PERF_URL", ""), os.environ.get("PERF_KEY", "")
    if not evs or not url or not key:
        return
    base = url.split("/perf/")[0]
    text = "\n".join(f"{e['time']} {e['detail']}" for e in evs[:5]) + "\nDetails: SMX HQ, activity feed."
    body = json.dumps({"subject": f"{len(evs)} automation run{'s' if len(evs) > 1 else ''} failed", "text": text}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(base + "/smx/alert", data=body, method="POST",
                                                      headers={"Content-Type": "application/json", "x-smx-key": key}), timeout=30)
    except Exception as e:
        print("alert not sent:", type(e).__name__)


def main():
    os.makedirs("ops", exist_ok=True)
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    meta_before = json.dumps(state.get("meta"), sort_keys=True)
    sha_before = state.get("last_sha")
    new = commit_events(state) + meta_events(state) + ci_events()
    lines = open(FEED).read().splitlines() if os.path.exists(FEED) else []
    seen = {json.loads(l)["id"] for l in lines if l.strip()}
    new = [e for e in new if e["id"] not in seen]
    alert_failures([e for e in new if e.get("source") == "ci"])
    lines += [json.dumps(e, ensure_ascii=False) for e in new]
    # Write (and so commit) only for real news. A moved last_sha alone is not news: this job's own "events" commit
    # moves HEAD, and saving that would make every run commit again, forever (found in the 18 Nov review).
    if new or json.dumps(state.get("meta"), sort_keys=True) != meta_before or not sha_before:
        open(FEED, "w").write("\n".join(lines[-KEEP:]) + "\n")
        json.dump(state, open(STATE, "w"), indent=1)
    else:
        open("ops/.events-unchanged", "w").write("")
    print(f"{len(new)} new events")


if __name__ == "__main__":
    main()
