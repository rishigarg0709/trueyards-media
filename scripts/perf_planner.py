#!/usr/bin/env python3
"""Media planner: splits Rishi's total daily budget across the WhatsApp autopilot and Meta ads tactics.

Runs every Monday 06:30 IST (before the autopilot's 07:30 plan) and on request (`--now`). Writes perf/plan.json, which
- the WhatsApp Lambda reads at 07:30 (accepts its share only inside its own PERF_WA_MIN..PERF_WA_MAX), and
- scripts/ads_ops.py reads every morning (Meta tactic budgets, never above config/ads.json caps).
Also appends perf/ledger.jsonl and rewrites perf/LEARNINGS.md: the shared memory every agent reads.

Rules (strategy/CHANNEL_COORDINATION.md): total is a hard ceiling; shift at most 20% of the total a week toward the
cheaper channel per site visit planned (per qualified lead while visits are few); floors at 30% of the starting share;
a channel younger than 14 days is never cut; no shift on noise (<15% difference).
Data: /perf/summary from the Lambda (secrets PERF_URL, PERF_KEY: aggregates only) and Meta insights (META_TOKEN).
"""
import json, os, sys, datetime, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CFG = json.load(open("config/perf.json"))
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
TACTIC_PREFIX = {"prospect": ("FIT A", "FIT B"), "remind": ("FIT R",), "unreach": ("FIT U",), "warm": ("FIT W",), "retarget": ("FIT C",)}

def today():
    return datetime.datetime.now(IST).date()

def fetch_summary(days):
    url, key = os.environ.get("PERF_URL"), os.environ.get("PERF_KEY")
    if not url or not key:
        return None
    req = urllib.request.Request(f"{url}?days={days}", headers={"x-perf-key": key})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def meta_spend(days):
    """Spend and WhatsApp chats per tactic over the window, from both FIT campaigns. Empty without a token."""
    if not os.environ.get("META_TOKEN"):
        return {}
    import ads_ops as A
    out = {}
    r = A.call(f"{A.ACT}/insights", {"level": "adset", "time_range": json.dumps({"since": str(today() - datetime.timedelta(days=days)), "until": str(today())}),
                                      "fields": "adset_name,campaign_name,spend,actions", "limit": 500})
    for row in r.get("data", []):
        if not row.get("campaign_name", "").startswith("FIT"):
            continue
        name = row.get("adset_name", "")
        tactic = next((t for t, pre in TACTIC_PREFIX.items() if any(name.startswith(p) for p in pre)), "other")
        x = out.setdefault(tactic, {"spend": 0.0, "chats": 0})
        x["spend"] += float(row.get("spend", 0))
        x["chats"] += A.conversations(row)
    return out

def channel_evidence(summary, spend):
    """Cost per visit planned and per qualified lead, per channel, over the window."""
    ev = {}
    if summary:
        days = summary["wa"]["days"]
        delivered = sum(d["delivered"] for d in days.values())
        wa_spend = delivered * float(summary["wa"].get("costPerDelivered") or 1.02)
        src = summary.get("leads_by_source", {})
        ev["wa"] = {"spend": round(wa_spend), **src.get("wa_outbound", {})}
        ev["meta"] = {"spend": round(sum(t["spend"] for t in spend.values())), **src.get("ctwa", {})}
    for c in ev.values():
        for k in ("leads", "qualified", "visit_planned", "visit_done", "booked"):
            c.setdefault(k, 0)
        c["per_visit"] = round(c["spend"] / c["visit_planned"]) if c["visit_planned"] else None
        c["per_qualified"] = round(c["spend"] / c["qualified"]) if c["qualified"] else None
        c["per_lead"] = round(c["spend"] / c["leads"]) if c["leads"] else None
    return ev

def split_channels(total, prev, ev, meta_days_live, cfg=CFG):
    """Returns (wa, meta, reasons). Deterministic, testable."""
    reasons = []
    st = cfg["start_share"]
    if prev and prev.get("total") and prev.get("wa_budget_inr") is not None:
        f = total / prev["total"]
        wa, meta = prev["wa_budget_inr"] * f, prev["meta_budget_inr"] * f
        if abs(f - 1) > 1e-9:
            reasons.append(f"Total changed to INR {total}; kept last week's proportions.")
    else:
        wa, meta = total * st["wa"], total * st["meta"]
        reasons.append(f"First plan: WhatsApp {round(st['wa']*100)}% (proven), Meta {round(st['meta']*100)}% (test).")
    floors = {"wa": total * st["wa"] * cfg["floor_of_start"], "meta": total * st["meta"] * cfg["floor_of_start"]}
    W, Mt = ev.get("wa"), ev.get("meta")
    metric = None
    if W and Mt:
        if W["visit_planned"] >= cfg["min_visits_to_compare"] and Mt["visit_planned"] >= cfg["min_visits_to_compare"]:
            metric = "per_visit"
        elif W["qualified"] >= cfg["min_qualified_to_compare"] and Mt["qualified"] >= cfg["min_qualified_to_compare"]:
            metric = "per_qualified"
    if not metric:
        reasons.append("Not enough visits or qualified leads on both channels yet to compare; split unchanged.")
    else:
        cw, cm = W[metric], Mt[metric]
        label = "site visit planned" if metric == "per_visit" else "qualified lead"
        better, worse = ("wa", "meta") if cw < cm else ("meta", "wa")
        ratio = max(cw, cm) / max(1, min(cw, cm))
        if ratio < 1.15:
            reasons.append(f"Cost per {label} is close (WhatsApp INR {cw}, Meta INR {cm}); no shift.")
        elif worse == "meta" and meta_days_live < cfg["min_test_days"]:
            reasons.append(f"Meta is behind (INR {cm} vs {cw} per {label}) but only {meta_days_live} days old; no cut before {cfg['min_test_days']} days.")
        else:
            cur = {"wa": wa, "meta": meta}
            step = min(cfg["max_shift_share"] * total, cur[worse] - floors[worse], total * 0.2 * min(1.0, (ratio - 1)))
            if step >= 10:
                cur[worse] -= step; cur[better] += step
                wa, meta = cur["wa"], cur["meta"]
                reasons.append(f"Moved INR {round(step)}/day to {'WhatsApp' if better == 'wa' else 'Meta'}: INR {min(cw, cm)} vs {max(cw, cm)} per {label}.")
            else:
                reasons.append(f"{'Meta' if worse == 'meta' else 'WhatsApp'} is at its floor; no further cut.")
    wa = round(wa); meta = total - wa
    return wa, meta, reasons

def split_meta(meta, summary, spend, ev, prev, cfg=CFG):
    """Meta tactics. Warm-up share follows measured lift: kept while each extra lead costs no more than a WhatsApp lead."""
    reasons = []
    waves = (summary or {}).get("schedule") or []
    if not waves:
        sh = dict(cfg["meta_tactics_without_waves"])
        reasons.append("No joint waves running; Meta goes to prospecting and the unreachable list.")
    else:
        sh = dict((prev or {}).get("meta_shares") or cfg["meta_tactics_start"])
        lift = ((summary or {}).get("lift") or {}).get("all", {}).get("all")
        if lift and lift["waves"] >= cfg["warm_min_waves_to_judge"] and lift["wd"] and lift["cd"]:
            extra = lift["wl"] - lift["wd"] * (lift["cl"] / lift["cd"])
            wspend = sum(spend.get(t, {}).get("spend", 0) for t in ("warm", "remind"))
            wa_cpl = (ev.get("wa") or {}).get("per_lead")
            cpe = wspend / extra if extra > 0 else None
            if cpe is not None and wa_cpl and cpe <= wa_cpl:
                sh["warm"] = min(0.4, sh["warm"] * 1.25)
                reasons.append(f"Warm-up pays: lift {lift['lift']}, about INR {round(cpe)} per extra lead vs INR {wa_cpl} per WhatsApp lead. Warm-up share up.")
            elif cpe is None or (wa_cpl and cpe > 2 * wa_cpl):
                sh["warm"] = max(0.05, sh["warm"] * 0.5)
                reasons.append(f"Warm-up not paying yet (lift {lift['lift']}{', cost per extra lead INR ' + str(round(cpe)) if cpe else ''}). Warm-up share halved.")
            else:
                reasons.append(f"Warm-up roughly break-even (lift {lift['lift']}); share held.")
        else:
            reasons.append("Warm-up lift not measurable yet (needs 3 waves a week old); shares held.")
    tot = sum(sh.values()) or 1
    sh = {k: v / tot for k, v in sh.items()}
    budgets = {k: round(meta * v) for k, v in sh.items()}
    small = [k for k, v in budgets.items() if 0 < v < cfg["min_tactic_inr"]]
    for k in small:  # too small to learn: fold into prospecting
        budgets["prospect_A"] = budgets.get("prospect_A", 0) + budgets[k]; budgets[k] = 0
    if small:
        reasons.append(f"Folded {', '.join(small)} into prospecting (under INR {cfg['min_tactic_inr']}/day learns nothing).")
    budgets["prospect_A"] += meta - sum(budgets.values())
    return budgets, sh, reasons

def plan(now=None):
    os.makedirs("perf", exist_ok=True)
    d = now or today()
    prev = None
    if os.path.exists("perf/plan.json"):
        prev = json.load(open("perf/plan.json"))
    total = CFG.get("total_daily_inr")
    if not total:
        out = {"date": str(d), "status": "awaiting_total", "product": CFG["product"], "note": "Rishi has not set total_daily_inr in config/perf.json. Nothing changes."}
        json.dump(out, open("perf/plan.json", "w"), indent=1)
        return out
    win = CFG["window_days"]
    summary = None
    try:
        summary = fetch_summary(win)
    except Exception as e:
        print("summary unavailable:", e)
    spend = meta_spend(win)
    ev = channel_evidence(summary, spend)
    st = {}
    try:
        st = json.load(open("ads/state.json"))
    except Exception:
        pass
    launched = st.get("launched_on")
    meta_days = (d - datetime.date.fromisoformat(launched)).days if launched else 0
    wa, meta, r1 = split_channels(total, prev if prev and prev.get("status") == "ok" else None, ev, meta_days)
    tactics, shares, r2 = split_meta(meta, summary, spend, ev, prev)
    out = {"date": str(d), "status": "ok", "product": CFG["product"], "total": total, "wa_budget_inr": wa, "meta_budget_inr": meta,
           "meta_tactics": tactics, "meta_shares": {k: round(v, 3) for k, v in shares.items()}, "warm": CFG["warm"],
           "evidence": {"window_days": win, "channels": ev, "meta_spend": spend, "lift": (summary or {}).get("lift"),
                        "summary": "ok" if summary else "unavailable"},
           "reasons": r1 + r2}
    json.dump(out, open("perf/plan.json", "w"), indent=1)
    with open("perf/ledger.jsonl", "a") as f:
        f.write(json.dumps({"date": str(d), "total": total, "wa": wa, "meta": meta, "tactics": tactics, "channels": ev, "lift": (summary or {}).get("lift")}) + "\n")
    write_learnings(out, summary)
    return out

def write_learnings(p, summary):
    """Plain-English shared memory: what the team has learnt so far. Every agent's Claude run reads this first."""
    L = [f"# Performance learnings ({p['date']})", "", "Shared memory of the WhatsApp autopilot, the ads agent and the planner. Aggregates only.", "",
         f"## This week's split (total INR {p['total']}/day before GST)",
         f"- WhatsApp autopilot INR {p['wa_budget_inr']}, Meta INR {p['meta_budget_inr']} ({', '.join(f'{k} {v}' for k, v in p['meta_tactics'].items() if v)})"]
    L += [f"- {r}" for r in p["reasons"]]
    L += ["", "## Cost by channel (last %d days)" % p["evidence"]["window_days"], "| Channel | Spend | Leads | Qualified | Visits planned | Visits done | Per lead | Per qualified | Per visit |", "|---|---|---|---|---|---|---|---|---|"]
    for k, c in p["evidence"]["channels"].items():
        L.append(f"| {k} | {c['spend']} | {c['leads']} | {c['qualified']} | {c['visit_planned']} | {c['visit_done']} | {c['per_lead'] or '-'} | {c['per_qualified'] or '-'} | {c['per_visit'] or '-'} |")
    lift = (summary or {}).get("lift") or {}
    if lift.get("zone") or lift.get("industry"):
        L += ["", "## Warm-up lift (warmed half vs control half, shrunk toward 1)"]
        for dim in ("zone", "industry"):
            for k, v in sorted((lift.get(dim) or {}).items(), key=lambda kv: -kv[1]["lift"]):
                L.append(f"- {dim} {k}: lift {v['lift']} over {v['waves']} waves ({v['wl']}/{v['wd']} warm vs {v['cl']}/{v['cd']} control)")
    cells = ((summary or {}).get("wa") or {}).get("cells") or []
    if cells:
        L += ["", "## Best WhatsApp cells (autopilot)"]
        for c in cells[:8]:
            L.append(f"- {c['c']}: {c['rate']}% lead rate, {c['delivered']} delivered, {c.get('visits', 0)} visits, {c.get('freshLeft', 0)} fresh left")
    open("perf/LEARNINGS.md", "w").write("\n".join(L) + "\n")

if __name__ == "__main__":
    print(json.dumps(plan(), indent=1))
