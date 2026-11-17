#!/usr/bin/env python3
"""FIT Ads agent v1: Meta click-to-WhatsApp ads from the TrueYards page into the FIT WhatsApp bot.

Reads ads/requests/*.json, writes ads/results/<name>.json. `--daily` runs the autopilot (cron).
Token: META_TOKEN secret, never written or printed (scrubbed through meta_ops.scrub).

Hard rules enforced HERE, not in prompts (strategy/PERFORMANCE_MARKETING_BRIEF.md):
- Everything is created PAUSED. Nothing goes live until config/ads.json has budget_approved and
  launch_approved set to true (only Rishi flips those) and a `launch` request runs.
- Sum of ad set daily budgets never exceeds daily_cap_inr. Code only ever lowers or moves budget,
  never raises the total. The campaign carries a lifetime spend_cap equal to monthly_cap_inr.
- If month-to-date spend plus today's budget would pass monthly_cap_inr, the campaign is paused.
- No op touches billing, payment methods, account spend caps or any campaign other than FIT's.
- Reports hold aggregates only. No phone numbers or names ever reach this (public) repo.
"""
import json, os, re, sys, glob, time, base64, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_ops as M

call, scrub = M.call, M.scrub
CFG_PATH = "config/ads.json"
CFG = json.load(open(CFG_PATH))
ACT = CFG["ad_account_id"]
STATE_PATH = "ads/state.json"
CONV = "onsite_conversion.messaging_conversation_started_7d"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

def today():
    return datetime.datetime.now(IST).date()

def load_state():
    try:
        return json.load(open(STATE_PATH))
    except Exception:
        return {"adsets": {}, "ads": {}}

def save_state(s):
    os.makedirs("ads", exist_ok=True)
    json.dump(s, open(STATE_PATH, "w"), indent=1, sort_keys=True)

def paise(inr):
    return int(round(float(inr) * 100))

def inr(p):
    return round(int(p) / 100, 2)

def err(r):
    e = r.get("error") or {}
    return e.get("error_user_msg") or e.get("message") or json.dumps(e)[:300]

# ---------- lookups ----------
def ty_page():
    r = call("me/accounts", {"fields": "id,name,access_token", "limit": 50})
    pages = r.get("data", [])
    for p in pages:
        if CFG["page_name_hint"].lower() in p["name"].lower():
            return p
    return pages[0] if pages else None

def find_campaign():
    r = call(f"{ACT}/campaigns", {"fields": "id,name,status,effective_status,spend_cap,created_time", "limit": 100})
    for c in r.get("data", []):
        if c["name"] == CFG["campaign_name"]:
            return c
    return None

def adsets_of(cid):
    return call(f"{cid}/adsets", {"fields": "id,name,status,effective_status,daily_budget", "limit": 50}).get("data", [])

def ads_of(cid):
    return call(f"{cid}/ads", {"fields": "id,name,status,effective_status,adset_id,created_time", "limit": 200}).get("data", [])

def spend(obj_id, preset):
    r = call(f"{obj_id}/insights", {"fields": "spend", "date_preset": preset})
    d = r.get("data", [])
    return float(d[0]["spend"]) if d else 0.0

def conversations(row):
    for a in row.get("actions", []) or []:
        if a.get("action_type") == CONV:
            return int(float(a["value"]))
    return 0

def insights(cid, level, preset):
    r = call(f"{cid}/insights", {"level": level, "date_preset": preset, "limit": 500,
             "fields": "ad_id,ad_name,adset_id,adset_name,spend,impressions,reach,frequency,clicks,ctr,actions"})
    out = {}
    for row in r.get("data", []):
        k = row.get("ad_id") if level == "ad" else row.get("adset_id")
        out[k] = {"name": row.get("ad_name") or row.get("adset_name"), "spend": float(row.get("spend", 0)),
                  "impressions": int(row.get("impressions", 0)), "frequency": float(row.get("frequency", 0) or 0),
                  "ctr": float(row.get("ctr", 0) or 0), "conversations": conversations(row)}
    return out

# ---------- targeting ----------
def geo(cities):
    out, missing = [], []
    for c in cities:
        r = call("search", {"type": "adgeolocation", "q": c["q"], "location_types": json.dumps(["city"]), "country_code": "IN", "limit": 5})
        hit = next((x for x in r.get("data", []) if x.get("country_code") == "IN"), None)
        if hit:
            out.append({"key": hit["key"], "radius": int(c.get("radius_km", 20)), "distance_unit": "kilometer"})
        else:
            missing.append(c["q"])
    return out, missing

def interests(names):
    ids, missing = [], []
    for n in names:
        r = call("search", {"type": "adinterest", "q": n, "limit": 5})
        data = r.get("data", [])
        base = lambda x: re.sub(r"\s*\(.*\)$", "", x["name"]).strip().lower()
        good = [x for x in data if base(x) == n.lower() and "(band)" not in x["name"].lower() and "(film)" not in x["name"].lower()]
        hit = max(good, key=lambda x: x.get("audience_size_upper_bound", 0) or 0) if good else None
        if hit and hit["id"] not in [i["id"] for i in ids]:
            ids.append({"id": hit["id"], "name": hit["name"]})
        elif not hit:
            missing.append(n)
    return ids, missing

def behaviors(names):
    if not names:
        return [], []
    r = call("search", {"type": "adTargetingCategory", "class": "behaviors", "limit": 1000})
    data = r.get("data", [])
    ids, missing = [], []
    for n in names:
        hit = next((x for x in data if x["name"].lower() == n.lower()), None)
        (ids.append({"id": hit["id"], "name": hit["name"]}) if hit else missing.append(n))
    return ids, missing

def audience_ids_by_name(names):
    if not names:
        return []
    have = {a["name"]: a["id"] for a in call(f"{ACT}/customaudiences", {"fields": "id,name", "limit": 200}).get("data", [])}
    return [have[n] for n in names if n in have]

def targeting(aset, audience_ids=None):
    notes = {}
    t = {"age_min": aset["age_min"], "age_max": aset["age_max"],
         "publisher_platforms": ["facebook", "instagram"],
         "targeting_automation": {"advantage_audience": int(aset.get("advantage_audience", 0))}}
    ex = audience_ids_by_name(CFG.get("exclude_audience_names", []))
    if ex:
        t["excluded_custom_audiences"] = [{"id": i} for i in ex]
    notes["excluded_audiences"] = len(ex)
    if audience_ids:
        t["geo_locations"] = {"regions": [], "countries": ["IN"]}
        t["custom_audiences"] = [{"id": i} for i in audience_ids]
        return t, notes
    g, notes["cities_not_found"] = geo(aset["cities"])
    t["geo_locations"] = {"cities": g, "location_types": ["home", "recent"]}
    flex = {}
    ii, notes["interests_not_found"] = interests(aset.get("interests", []))
    bb, notes["behaviors_not_found"] = behaviors(aset.get("behaviors", []))
    if ii:
        flex["interests"] = ii
    if bb:
        flex["behaviors"] = bb
    if flex:
        t["flexible_spec"] = [flex]
    notes["interests_used"] = [i["name"] for i in ii] + [b["name"] for b in bb]
    return t, notes

# ---------- creatives ----------
def upload_image(path):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    r = call(f"{ACT}/adimages", {"bytes": b64}, "POST")
    if "images" not in r:
        raise RuntimeError(f"image upload failed for {path}: {err(r)}")
    return next(iter(r["images"].values()))["hash"]

def make_ad(page_id, adset_id, ad, status):
    h = upload_image(ad["image"])
    link = {"image_hash": h, "link": "https://api.whatsapp.com/send", "message": ad["text"], "name": ad["headline"],
            "call_to_action": {"type": "WHATSAPP_MESSAGE", "value": {"app_destination": "WHATSAPP"}}}
    spec = {"page_id": page_id, "link_data": link}
    if CFG.get("instagram_user_id"):
        spec["instagram_user_id"] = CFG["instagram_user_id"]
    welcome = json.dumps({"type": "VISUAL_EDITOR", "version": 2, "landing_screen_type": "welcome_message", "media_type": "text",
                          "text_format": {"customer_action_type": "autofill_message",
                                          "message": {"autofill_message": {"content": CFG["prefill_message"]}, "text": "Hi, thanks for your interest in FIT."}}})
    tries = [dict(link_data={**link, "page_welcome_message": welcome}), dict(link_data=link)]
    errs, cr = [], None
    for t in tries:
        s = {**spec, **t}
        cr = call(f"{ACT}/adcreatives", {"name": f"FIT {ad['name']}", "object_story_spec": s}, "POST")
        if "id" in cr:
            break
        errs.append(err(cr))
        if "instagram" in json.dumps(cr).lower() and "instagram_user_id" in spec:
            spec.pop("instagram_user_id")
    if "id" not in cr:
        return {"error": errs}
    a = call(f"{ACT}/ads", {"name": ad["name"], "adset_id": adset_id, "creative": {"creative_id": cr["id"]}, "status": status}, "POST")
    return {"ad": a, "creative_id": cr["id"], "earlier_errors": errs}

# ---------- guards ----------
def live_ok():
    return bool(CFG.get("budget_approved")) and bool(CFG.get("launch_approved"))

def month_guard(camp, daily_total_inr):
    spent = spend(camp["id"], "this_month")
    cap = float(CFG["monthly_cap_inr"])
    return spent, (spent + daily_total_inr) <= cap

def active_budget_total(sets):
    return sum(inr(s.get("daily_budget", 0)) for s in sets if s.get("status") == "ACTIVE")

# ---------- ops ----------
def op_status(req):
    camp = find_campaign()
    acct = call(ACT, {"fields": "name,account_status,currency,amount_spent,balance,spend_cap,disable_reason,funding_source_details"})
    acct.pop("funding_source_details", None)
    out = {"config": {k: CFG[k] for k in ("budget_approved", "launch_approved", "daily_cap_inr", "monthly_cap_inr")},
           "account": acct, "campaign": camp}
    if camp:
        out["adsets"] = adsets_of(camp["id"])
        out["ads"] = ads_of(camp["id"])
        out["spend_today_inr"] = spend(camp["id"], "today")
        out["spend_month_inr"] = spend(camp["id"], "this_month")
    return out

def op_setup(req):
    """Idempotent. Builds campaign, ad sets and ads, all PAUSED. No spend can happen from this op."""
    st = load_state()
    p = ty_page()
    if not p:
        return {"error": "TrueYards page not visible to the system user"}
    enabled = [a for a in CFG["adsets"] if a.get("enabled")]
    total = sum(a["daily_budget_inr"] for a in enabled)
    if total > CFG["daily_cap_inr"]:
        return {"blocked": f"ad set budgets add up to INR {total}, above the daily cap INR {CFG['daily_cap_inr']}"}
    out = {"page": {"id": p["id"], "name": p["name"]}, "adsets": {}, "ads": {}}
    camp = find_campaign()
    if not camp:
        camp = call(f"{ACT}/campaigns", {"name": CFG["campaign_name"], "objective": "OUTCOME_ENGAGEMENT", "status": "PAUSED",
                    "special_ad_categories": CFG["special_ad_categories"], "buying_type": "AUCTION",
                    "is_adset_budget_sharing_enabled": "false", "spend_cap": paise(CFG["monthly_cap_inr"])}, "POST")
        if "id" not in camp:
            return {"campaign_error": err(camp)}
    st["campaign_id"] = camp["id"]
    out["campaign"] = camp
    existing = {s["name"]: s for s in adsets_of(camp["id"])}
    existing_ads = {a["name"] for a in ads_of(camp["id"])}
    for a in enabled:
        s = existing.get(a["name"])
        if not s:
            t, notes = targeting(a)
            base = {"name": a["name"], "campaign_id": camp["id"], "status": "PAUSED", "daily_budget": paise(a["daily_budget_inr"]),
                    "billing_event": "IMPRESSIONS", "optimization_goal": "CONVERSATIONS", "destination_type": "WHATSAPP",
                    "bid_strategy": "LOWEST_COST_WITHOUT_CAP", "targeting": t}
            errs = []
            for po in ({"page_id": p["id"], "whatsapp_phone_number": CFG["whatsapp_number"]}, {"page_id": p["id"]}):
                s = call(f"{ACT}/adsets", {**base, "promoted_object": po}, "POST")
                if "id" in s:
                    break
                errs.append(err(s))
            out["adsets"][a["key"]] = {"result": s, "targeting_notes": notes, "earlier_errors": errs[:-1] if "id" in s else errs}
            if "id" not in s:
                continue
        st["adsets"][a["key"]] = s["id"]
        for ad in a["ads"]:
            if ad["name"] in existing_ads:
                continue
            try:
                r = make_ad(p["id"], s["id"], ad, "PAUSED")
            except Exception as e:
                r = {"error": str(e)}
            out["ads"][ad["name"]] = r
            if "ad" in r and "id" in r["ad"]:
                st["ads"][ad["name"]] = r["ad"]["id"]
    st["last_creatives_added"] = str(today())
    save_state(st)
    out["next"] = "Everything is PAUSED. Rishi reviews in Ads Manager, sets budget_approved and launch_approved in config/ads.json, then a launch request turns it on."
    return out

def op_launch(req):
    if not live_ok():
        return {"blocked": "config/ads.json needs budget_approved: true and launch_approved: true (Rishi only)"}
    camp = find_campaign()
    if not camp:
        return {"error": "run setup first"}
    sets = [s for s in adsets_of(camp["id"]) if any(a["name"] == s["name"] and a.get("enabled") for a in CFG["adsets"])]
    total = sum(inr(s["daily_budget"]) for s in sets)
    if total > CFG["daily_cap_inr"]:
        return {"blocked": f"budgets INR {total} above daily cap"}
    spent, ok = month_guard(camp, total)
    if not ok:
        return {"blocked": f"monthly cap: spent INR {spent:.0f}"}
    out = {"ads": [], "adsets": []}
    set_ids = {s["id"] for s in sets}
    for a in ads_of(camp["id"]):
        if a["adset_id"] in set_ids and a["status"] != "ARCHIVED":
            out["ads"].append(call(a["id"], {"status": "ACTIVE"}, "POST") | {"name": a["name"]})
    for s in sets:
        out["adsets"].append(call(s["id"], {"status": "ACTIVE"}, "POST") | {"name": s["name"]})
    out["campaign"] = call(camp["id"], {"status": "ACTIVE"}, "POST")
    st = load_state(); st.setdefault("launched_on", str(today())); save_state(st)
    return out

def lead_data(req):
    """Aggregates per ad id from the Leads sheet: {ad_id: {chats, qualified, visit_planned, visit_done, booked}}.
    Comes in the request or in ads/data/leads_by_ad.json (written by the daily Claude run). Counts only."""
    d = req.get("leads_by_ad")
    if d is None and os.path.exists("ads/data/leads_by_ad.json"):
        f = json.load(open("ads/data/leads_by_ad.json"))
        if time.time() - f.get("generated_at_epoch", 0) < 36 * 3600:
            d = f.get("by_ad")
    return d

def op_daily(req):
    dry = bool(req.get("dry_run"))
    st = load_state()
    camp = find_campaign()
    rep = {"date": str(today()), "dry_run": dry, "actions": [], "flags": []}
    if not camp:
        rep["flags"].append("Campaign not created yet (run setup).")
        return rep
    sets = adsets_of(camp["id"])
    ads = ads_of(camp["id"])
    rep["campaign_status"] = camp.get("effective_status")
    live = camp.get("status") == "ACTIVE"
    total = active_budget_total(sets)
    spent_m, ok = month_guard(camp, total)
    rep["spend_month_inr"] = spent_m
    rep["spend_yesterday_inr"] = spend(camp["id"], "yesterday")
    rep["daily_budget_total_inr"] = total
    rep["monthly_cap_inr"] = CFG["monthly_cap_inr"]

    # 1. hard caps
    if live and not ok:
        rep["actions"].append(f"PAUSED campaign: month spend INR {spent_m:.0f} plus today's INR {total:.0f} would pass the INR {CFG['monthly_cap_inr']} cap")
        if not dry:
            call(camp["id"], {"status": "PAUSED"}, "POST")
        live = False
    if total > CFG["daily_cap_inr"]:
        f = CFG["daily_cap_inr"] / total
        for s in sets:
            if s["status"] == "ACTIVE":
                nb = int(inr(s["daily_budget"]) * f)
                rep["actions"].append(f"Lowered {s['name']} to INR {nb} to respect the daily cap")
                if not dry:
                    call(s["id"], {"daily_budget": paise(nb)}, "POST")

    # 2. data
    life = insights(camp["id"], "ad", "maximum")
    d7 = insights(camp["id"], "ad", "last_7d")
    y = insights(camp["id"], "ad", "yesterday")
    s3 = insights(camp["id"], "adset", "last_3d")
    leads = lead_data(req)
    rep["lead_data"] = "joined from Leads sheet" if leads is not None else "not available, rules use WhatsApp conversations only"
    T_CPL, T_CPC, MULT = CFG["target_cost_per_qualified_lead_inr"], CFG["target_cost_per_conversation_inr"], CFG["pause_multiple"]

    rows = []
    for a in ads:
        L, Y, W = life.get(a["id"], {}), y.get(a["id"], {}), d7.get(a["id"], {})
        ld = (leads or {}).get(a["id"], {})
        sp, cv = L.get("spend", 0.0), L.get("conversations", 0)
        q = ld.get("qualified") if leads is not None else None
        row = {"ad": a["name"], "status": a["effective_status"], "spend_yday": Y.get("spend", 0.0), "conv_yday": Y.get("conversations", 0),
               "spend_life": sp, "conv_life": cv, "cpc_life": round(sp / cv) if cv else None,
               "qualified": q, "visit_planned": ld.get("visit_planned"), "visit_done": ld.get("visit_done"),
               "freq_7d": W.get("frequency", 0.0), "ctr_7d": W.get("ctr", 0.0)}
        rows.append(row)
        if a["status"] != "ACTIVE":
            continue
        why = None
        if q is not None:
            if sp >= MULT * T_CPL and q == 0:
                why = f"spent INR {sp:.0f} (over {MULT}x the INR {T_CPL} target per qualified lead) with no qualified lead"
        else:
            if sp >= MULT * T_CPL and cv == 0:
                why = f"spent INR {sp:.0f} with no WhatsApp conversation"
            elif cv and sp >= T_CPL and sp / cv > MULT * T_CPC:
                why = f"INR {sp / cv:.0f} per conversation, over {MULT}x the INR {T_CPC} target"
        if why:
            rep["actions"].append(f"PAUSED ad {a['name']}: {why}")
            if not dry:
                call(a["id"], {"status": "PAUSED"}, "POST")
            row["status"] = "PAUSED (today)"
        if W.get("frequency", 0) > 3 and not why:
            rep["flags"].append(f"{a['name']}: 7-day frequency {W['frequency']:.1f}, creative fatigue, replace it this week")
    rep["ads"] = rows

    # 3. budget shift (once a day, within the same total)
    launched = st.get("launched_on")
    days_live = (today() - datetime.date.fromisoformat(launched)).days if launched else 0
    act = [s for s in sets if s["status"] == "ACTIVE"]
    if live and len(act) >= 2 and days_live >= CFG["min_days_before_shift"] and st.get("last_shift") != str(today()):
        def score(s):
            d = s3.get(s["id"], {})
            res = sum(((leads or {}).get(a["id"], {}).get("qualified") or 0) for a in ads if a["adset_id"] == s["id"]) if leads is not None else d.get("conversations", 0)
            return (d.get("spend", 0) / res) if res else float("inf"), d.get("spend", 0), res
        ranked = sorted(act, key=lambda s: score(s)[0])
        best, worst = ranked[0], ranked[-1]
        bs, ws = score(best), score(worst)
        if best["id"] != worst["id"] and bs[0] < ws[0] and ws[1] >= T_CPC:
            wb, bb = inr(worst["daily_budget"]), inr(best["daily_budget"])
            amt = int(min(wb * CFG["max_shift_pct_per_day"] / 100, wb - CFG["min_adset_daily_inr"]))
            if amt >= 10:
                rep["actions"].append(f"Moved INR {amt}/day from {worst['name']} (INR {ws[0] if ws[0] != float('inf') else 'n/a'} per result) to {best['name']} (INR {bs[0]:.0f} per result). Daily total unchanged.")
                if not dry:
                    call(worst["id"], {"daily_budget": paise(wb - amt)}, "POST")
                    call(best["id"], {"daily_budget": paise(bb + amt)}, "POST")
                    st["last_shift"] = str(today())

    # 4. creative cadence: 2 fresh creatives a week
    lc = st.get("last_creatives_added")
    if live and (not lc or (today() - datetime.date.fromisoformat(lc)).days >= 7):
        rep["flags"].append("2 fresh creatives due this week (FIT creative studio, HRERA top right), then an add_ads request.")
    if live and not dry:
        save_state(st)
    write_report(rep)
    return rep

def write_report(rep):
    os.makedirs("ads/reports", exist_ok=True)
    L = [f"# FIT ads, {rep['date']}{' (dry run)' if rep['dry_run'] else ''}", "",
         f"Campaign: {rep.get('campaign_status')}. Yesterday INR {rep.get('spend_yesterday_inr', 0):.0f}. Month INR {rep.get('spend_month_inr', 0):.0f} of {rep.get('monthly_cap_inr')} cap. Daily budget INR {rep.get('daily_budget_total_inr', 0):.0f}.",
         f"Lead data: {rep.get('lead_data', '-')}", "",
         "| Ad | Status | Spend yday | Chats yday | Spend total | Chats total | INR/chat | Qualified | Visit planned | Visit done | Freq 7d |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rep.get("ads", []):
        f = lambda v: "-" if v is None else v
        L.append(f"| {r['ad']} | {r['status']} | {r['spend_yday']:.0f} | {r['conv_yday']} | {r['spend_life']:.0f} | {r['conv_life']} | {f(r['cpc_life'])} | {f(r['qualified'])} | {f(r['visit_planned'])} | {f(r['visit_done'])} | {r['freq_7d']:.1f} |")
    L += ["", "## Actions"] + ([f"- {a}" for a in rep["actions"]] or ["- none"])
    L += ["", "## Flags"] + ([f"- {a}" for a in rep["flags"]] or ["- none"])
    open(f"ads/reports/{rep['date']}.md", "w").write("\n".join(L) + "\n")

def op_add_ads(req):
    """Add fresh creatives to an ad set. Live only when the campaign is already approved and running; never touches budget."""
    camp = find_campaign()
    st = load_state()
    key = req["adset_key"]
    sid = st.get("adsets", {}).get(key)
    if not camp or not sid:
        return {"error": "campaign or ad set missing, run setup"}
    status = "ACTIVE" if (live_ok() and camp.get("status") == "ACTIVE") else "PAUSED"
    p = ty_page()
    out = {}
    for ad in req["ads"]:
        r = make_ad(p["id"], sid, ad, status)
        out[ad["name"]] = r
        if "ad" in r and "id" in r["ad"]:
            st["ads"][ad["name"]] = r["ad"]["id"]
    st["last_creatives_added"] = str(today())
    save_state(st)
    return {"status_used": status, "ads": out}

def op_pause_ad(req):
    camp = find_campaign()
    if not camp or req["ad_id"] not in {a["id"] for a in ads_of(camp["id"])}:
        return {"error": "ad is not in the FIT campaign"}
    return call(req["ad_id"], {"status": "PAUSED"}, "POST")

def op_pause_all(req):
    camp = find_campaign()
    return call(camp["id"], {"status": "PAUSED"}, "POST") if camp else {"note": "no campaign"}

def op_audiences(req):
    """Builds retargeting audiences (no spend). Engagers of the TY page and Instagram for 365 days, and
    optionally FIT WhatsApp chatters from SHA-256 hashed phone numbers passed in the request (never plain)."""
    p = ty_page()
    have = {a["name"]: a for a in call(f"{ACT}/customaudiences", {"fields": "id,name,approximate_count_lower_bound", "limit": 100}).get("data", [])}
    out = {}
    specs = {
        "TY page engagers 365d": {"event_sources": [{"id": p["id"], "type": "page"}], "retention_seconds": 31536000,
                                  "filter": {"operator": "and", "filters": [{"field": "event", "operator": "eq", "value": "page_engaged"}]}},
        "TY Instagram engagers 365d": {"event_sources": [{"id": CFG["instagram_user_id"], "type": "ig_business"}], "retention_seconds": 31536000,
                                       "filter": {"operator": "and", "filters": [{"field": "event", "operator": "eq", "value": "ig_business_profile_all"}]}},
    }
    for name, rule in specs.items():
        if name in have:
            out[name] = have[name]; continue
        out[name] = call(f"{ACT}/customaudiences", {"name": name, "rule": {"inclusions": {"operator": "or", "rules": [rule]}},
                         "prefill": "true"}, "POST")
    lists = dict(req.get("lists") or {})
    if req.get("phones_sha256"):
        lists["FIT WhatsApp chatters"] = req["phones_sha256"]
    for name, hashed in lists.items():
        if any(len(h) != 64 for h in hashed):
            out[name] = {"error": "send SHA-256 hashes only, never plain numbers"}; continue
        a = have.get(name) or call(f"{ACT}/customaudiences", {"name": name, "subtype": "CUSTOM", "customer_file_source": "USER_PROVIDED_ONLY"}, "POST")
        out[name] = a
        if "id" in a:
            # replace the list each time so people who moved stage drop out
            out[name + " upload"] = call(f"{a['id']}/usersreplace", {"payload": {"schema": "PHONE_SHA256", "data": hashed},
                                         "session": {"session_id": int(time.time()), "batch_seq": 1, "last_batch_flag": True}}, "POST")
    return out

def op_enable_retargeting(req):
    """Week 2: ad set C from the audiences, budget moved out of A and B so the daily total stays the same."""
    camp, st = find_campaign(), load_state()
    if not camp:
        return {"error": "run setup first"}
    c = next(a for a in CFG["adsets"] if a["key"] == "C")
    if st["adsets"].get("C"):
        return {"note": "already exists", "id": st["adsets"]["C"]}
    have = {a["name"]: a["id"] for a in call(f"{ACT}/customaudiences", {"fields": "id,name", "limit": 100}).get("data", [])}
    ids = [have[n] for n in c["audience_names"] if n in have]
    if not ids:
        return {"error": "run audiences first"}
    sets = [s for s in adsets_of(camp["id"]) if s["status"] == "ACTIVE"]
    take = c["daily_budget_inr"]
    if sum(inr(s["daily_budget"]) - CFG["min_adset_daily_inr"] for s in sets) < take:
        return {"blocked": "not enough budget in A and B to fund C without raising the total"}
    out = {"moved": []}
    each = take / len(sets)
    p = ty_page()
    t, _ = targeting(c, ids)
    status = "ACTIVE" if (live_ok() and camp.get("status") == "ACTIVE") else "PAUSED"
    s = call(f"{ACT}/adsets", {"name": c["name"], "campaign_id": camp["id"], "status": status, "daily_budget": paise(take),
             "billing_event": "IMPRESSIONS", "optimization_goal": "CONVERSATIONS", "destination_type": "WHATSAPP",
             "bid_strategy": "LOWEST_COST_WITHOUT_CAP", "targeting": t, "promoted_object": {"page_id": p["id"]}}, "POST")
    if "id" not in s:
        return {"error": err(s)}
    for x in sets:
        nb = int(inr(x["daily_budget"]) - each)
        out["moved"].append(call(x["id"], {"daily_budget": paise(nb)}, "POST") | {"name": x["name"], "new_inr": nb})
    st["adsets"]["C"] = s["id"]; save_state(st)
    ads = req.get("ads") or [dict(a, name="C" + a["name"][1:]) for a in CFG["adsets"][0]["ads"][:2]]
    out["ads"] = {ad["name"]: make_ad(p["id"], s["id"], ad, status) for ad in ads}
    out["adset"] = s
    return out

def op_check(req):
    """Read-only preflight: page, WhatsApp link on the page, account state, and targeting resolution for each ad set."""
    p = ty_page()
    out = {"page": None, "account": call(ACT, {"fields": "name,account_status,currency,timezone_name,disable_reason"})}
    if p:
        info = call(p["id"], {"fields": "id,name,whatsapp_number,link"}, token=p["access_token"])
        out["page"] = {"id": p["id"], "name": p["name"], "whatsapp_number_on_page": info.get("whatsapp_number"), "lookup_error": err(info) if "error" in info else None}
        out["whatsapp_linked_to_expected_number"] = bool(info.get("whatsapp_number")) and info.get("whatsapp_number", "").replace(" ", "").endswith(CFG["whatsapp_number"][-10:])
    out["targeting"] = {}
    for a in CFG["adsets"]:
        if a.get("cities"):
            t, notes = targeting(a)
            out["targeting"][a["key"]] = {"interest_ids": [i["id"] for f in t.get("flexible_spec", []) for v in f.values() for i in v], "cities_found": len(t["geo_locations"]["cities"]), **notes}
            est = call(f"{ACT}/delivery_estimate", {"optimization_goal": "REACH", "targeting_spec": t})
            d = (est.get("data") or [{}])[0]
            out["targeting"][a["key"]]["audience_estimate"] = [d.get("estimate_mau_lower_bound"), d.get("estimate_mau_upper_bound")] if d else err(est)
    out["creatives_present"] = {ad["image"]: os.path.exists(ad["image"]) for a in CFG["adsets"] for ad in a["ads"]}
    return out

OPS = {"check": op_check, "status": op_status, "setup": op_setup, "launch": op_launch, "daily": op_daily, "add_ads": op_add_ads,
       "pause_ad": op_pause_ad, "pause_all": op_pause_all, "audiences": op_audiences, "enable_retargeting": op_enable_retargeting}
# Deliberately absent: any op that raises budgets or caps, touches billing, or edits non-FIT campaigns.

def run(name, req):
    try:
        fn = OPS.get(req.get("op"))
        res = fn(req) if fn else {"error": f"unknown op {req.get('op')}"}
    except Exception as e:
        res = {"error": f"{type(e).__name__}: {e}"}
    res = scrub({"op": req.get("op"), "ran_at": datetime.datetime.utcnow().isoformat() + "Z", "result": res})
    os.makedirs("ads/results", exist_ok=True)
    json.dump(res, open(f"ads/results/{name}.json", "w"), indent=1)
    print(f"done {name}")

def main():
    if not M.TOKEN:
        sys.exit("META_TOKEN secret missing")
    os.makedirs("ads/processed", exist_ok=True)
    if "--daily" in sys.argv:
        run(f"daily-{today()}", {"op": "daily"})
        return
    for f in sorted(glob.glob("ads/requests/*.json")):
        name = os.path.basename(f)[:-5]
        if os.path.exists(f"ads/processed/{name}"):
            os.remove(f); continue
        open(f"ads/processed/{name}", "w").write(datetime.datetime.utcnow().isoformat())
        try:
            req = json.load(open(f))
        except Exception as e:
            req = {"op": None, "_err": str(e)}
        run(name, req)
        os.remove(f)

if __name__ == "__main__":
    main()
