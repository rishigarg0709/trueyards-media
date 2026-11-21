#!/usr/bin/env python3
"""FIT Ads agent v1: Meta click-to-WhatsApp ads from the TrueYards page into the FIT WhatsApp bot.

Reads ads/requests/*.json, writes ads/results/<name>.json. `--daily` runs the autopilot (cron).
Token: META_TOKEN secret, never written or printed (scrubbed through meta_ops.scrub).

Hard rules enforced HERE, not in prompts (strategy/PERFORMANCE_MARKETING_BRIEF.md):
- Everything is created PAUSED. Nothing goes live until config/ads.json has budget_approved and
  launch_approved set to true (only Rishi flips those) and a `launch` request runs.
- Sum of ad set daily budgets never exceeds daily_cap_inr. Code only lowers or moves budget, except the meta_ramp Rishi approved,
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

def use_product(product=None):
    """Point the agent at another product's config and state (config/ads_<product>.json, ads/state_<product>.json)."""
    global CFG, CFG_PATH, ACT, STATE_PATH
    CFG_PATH = f"config/ads_{product}.json" if product else "config/ads.json"
    STATE_PATH = f"ads/state_{product}.json" if product else "ads/state.json"
    CFG = json.load(open(CFG_PATH)); ACT = CFG["ad_account_id"]

def products():
    return [os.path.basename(p)[4:-5] for p in sorted(glob.glob("config/ads_*.json"))]

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

def _list(path, fields, limit):
    r = call(path, {"fields": fields, "limit": limit})
    if "data" not in r:
        # never treat a failed lookup (rate limit, outage) as "nothing exists": that creates duplicates
        raise RuntimeError(f"Meta lookup failed for {path}: {err(r)}")
    return r["data"]

def adsets_of(cid):
    return _list(f"{cid}/adsets", "id,name,status,effective_status,daily_budget", 50)

def ads_of(cid):
    return _list(f"{cid}/ads", "id,name,status,effective_status,adset_id,created_time", 200)

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
            out.append({"key": hit["key"], "radius": max(17, min(80, int(c.get("radius_km", 20)))), "distance_unit": "kilometer"})  # Meta allows 17 to 80 km
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
def welcome_variants(ad):
    """Most qualifying first: ice breakers (taps map to qualification answers), then an angle-specific prefill, then none."""
    out = []
    ib = CFG.get("ice_breakers")
    if ib:
        out.append(json.dumps({"type": "VISUAL_EDITOR", "version": 2, "landing_screen_type": "welcome_message", "media_type": "text",
                               "text_format": {"customer_action_type": "ice_breakers",
                                               "message": {"ice_breakers": [{"title": b["title"], "response": b["response"]} for b in ib],
                                                           "quick_replies": [], "text": CFG.get("welcome_text", "Hi, thanks for your interest in FIT.")}},
                               "user_edit": False, "surface": "visual_editor_new"}))
    out.append(json.dumps({"type": "VISUAL_EDITOR", "version": 2, "landing_screen_type": "welcome_message", "media_type": "text",
                           "text_format": {"customer_action_type": "autofill_message",
                                           "message": {"autofill_message": {"content": ad.get("prefill") or CFG["prefill_message"]},
                                                       "text": CFG.get("welcome_text", "Hi, thanks for your interest in FIT.")}}}))
    out.append(None)
    return out

def opt_out_spec():
    feats = CFG.get("creative_opt_out") or []
    return {"creative_features_spec": {f: {"enroll_status": "OPT_OUT"} for f in feats}} if feats else None

def create_creative(name, spec, key, base):
    """Try each welcome variant with the enhancement opt-outs, then without opt-outs. Returns (creative, errors, notes)."""
    errs = []
    for dof in (opt_out_spec(), None):
        for w in welcome_variants(base):
            data = dict(spec[key]); 
            if w: data["page_welcome_message"] = w
            body = {"name": name, "object_story_spec": {**spec, key: data}}
            if dof: body["degrees_of_freedom_spec"] = dof
            cr = call(f"{ACT}/adcreatives", body, "POST")
            if "id" in cr:
                return cr, errs, {"welcome": "ice_breakers" if w and "ice_breakers" in w else ("prefill" if w else "none"), "opt_outs": bool(dof)}
            errs.append(err(cr))
            if "instagram" in json.dumps(cr).lower() and "instagram_user_id" in spec:
                spec = {k: v for k, v in spec.items() if k != "instagram_user_id"}
    return {}, errs, {}

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
    cr, errs, notes = create_creative(f"FIT {ad['name']}", spec, "link_data", ad)
    if "id" not in cr:
        return {"error": errs}
    a = call(f"{ACT}/ads", {"name": ad["name"], "adset_id": adset_id, "creative": {"creative_id": cr["id"]}, "status": status}, "POST")
    return {"ad": a, "creative_id": cr["id"], "creative_notes": notes, "earlier_errors": errs}

# ---------- guards ----------
def live_ok():
    return bool(CFG.get("budget_approved")) and bool(CFG.get("launch_approved"))

def month_guard(camp, daily_total_inr):
    spent = fit_month_spend()  # both FIT campaigns (CTWA and warm-up) count against one monthly cap
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
        camp = call(f"{ACT}/campaigns", {"name": CFG["campaign_name"], "objective": CFG.get("campaign_objective", "OUTCOME_ENGAGEMENT"), "status": "PAUSED",
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
            t, notes = targeting(a, a.get("custom_audience_ids"))
            base = {"name": a["name"], "campaign_id": camp["id"], "status": "PAUSED", "daily_budget": paise(a["daily_budget_inr"]),
                    **({"start_time": a["start_time"]} if a.get("start_time") else {}),
                    **({"end_time": a["end_time"]} if a.get("end_time") else {}),
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
        for ad in a["ads"] + a.get("video_ads", []):
            if ad["name"] in existing_ads:
                continue
            try:
                r = (make_video_ad if "video" in ad else make_ad)(p["id"], s["id"], ad, "PAUSED")
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
    try:
        cur_cap = inr(call(camp["id"], {"fields": "spend_cap"}).get("spend_cap") or 0)
        if not dry and cur_cap and cur_cap < CFG["monthly_cap_inr"]:
            call(camp["id"], {"spend_cap": paise(CFG["monthly_cap_inr"])}, "POST")
            rep["actions"].append(f"Campaign spend cap INR {cur_cap:.0f} -> {CFG['monthly_cap_inr']} (config)")
    except Exception as e:
        rep["flags"].append(f"spend cap check failed: {e}")

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
    summary = perf_summary()
    leads = lead_data(req)
    if leads is None and summary is not None:
        leads = summary.get("ads") or {}
    rep["lead_data"] = "joined from the bot's lead records (per ad id)" if leads is not None else "not available, rules use WhatsApp conversations only"
    if summary:
        rep["lift"] = (summary.get("lift") or {}).get("all", {}).get("all")
        rep["waves"] = len(summary.get("schedule") or [])
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
        batch_day = today().weekday() == CFG.get("tester", {}).get("batch_weekday", 0)
        if not batch_day:
            # weekdays: emergency pauses only (no conversation at all after 4x the target cost per qualified lead)
            if sp >= 2 * MULT * T_CPL and cv == 0:
                why = f"emergency: spent INR {sp:.0f} with no WhatsApp conversation"
        elif q is not None:
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
    sp_l = sum(r.get("spend_life") or 0 for r in rows); cv_l = sum(r.get("conv_life") or 0 for r in rows)
    rep["meta_cost_per_chat"] = round(sp_l / cv_l) if cv_l else None
    sy = rep["spend_yesterday_inr"] or 0
    if live and total and sy < 0.5 * total:
        rep["flags"].append(f"Under-delivery: spent INR {sy:.0f} of INR {total:.0f} yesterday. Check for rejected ads or a too-small audience.")

    # 2b. tactics (warm-up, reminder, unreachable) and planner budgets, then the creative tester
    try:
        if CFG.get("use_planner", True):
            apply_tactics_and_plan(rep, summary, dry)
    except Exception as e:
        rep["flags"].append(f"Tactics step skipped: {type(e).__name__}: {e}")
    try:
        creative_tester(rep, life, leads, dry)
    except Exception as e:
        rep["flags"].append(f"Creative tester skipped: {type(e).__name__}: {e}")
    sets = adsets_of(camp["id"])  # budgets may have changed above

    # 3. budget shift (once a day, within the same total). A product whose config has no max_shift_pct_per_day
    # (Jind: Rishi fixed the J and R budgets, Directive D12) is never shifted.
    launched = st.get("launched_on")
    days_live = (today() - datetime.date.fromisoformat(launched)).days if launched else 0
    act = [s for s in sets if s["status"] == "ACTIVE"]
    if live and len(act) >= 2 and days_live >= CFG.get("min_days_before_shift", 3) and st.get("last_shift") != str(today()):
        def score(s):
            d = s3.get(s["id"], {})
            res = sum(((leads or {}).get(a["id"], {}).get("qualified") or 0) for a in ads if a["adset_id"] == s["id"]) if leads is not None else d.get("conversations", 0)
            return (d.get("spend", 0) / res) if res else float("inf"), d.get("spend", 0), res
        ranked = sorted(act, key=lambda s: score(s)[0])
        best, worst = ranked[0], ranked[-1]
        bs, ws = score(best), score(worst)
        if best["id"] != worst["id"] and bs[0] < ws[0] and ws[1] >= T_CPC:
            wb, bb = inr(worst["daily_budget"]), inr(best["daily_budget"])
            amt = int(min(wb * CFG.get("max_shift_pct_per_day", 0) / 100, wb - CFG["min_adset_daily_inr"]))
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
    if rep.get("plan"):
        L += ["", f"Planner: {rep['plan']}"]
    if rep.get("lift"):
        lf = rep["lift"]
        L += [f"Warm-up lift so far: {lf['lift']} over {lf['waves']} waves ({lf['wl']} leads from {lf['wd']} warmed vs {lf['cl']} from {lf['cd']} control)."]
    L += ["", "## Actions"] + ([f"- {a}" for a in rep["actions"]] or ["- none"])
    L += ["", "## Flags"] + ([f"- {a}" for a in rep["flags"]] or ["- none"])
    open(f"ads/reports/{CFG.get('report_prefix', '')}{rep['date']}.md", "w").write("\n".join(L) + "\n")

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
    use_product(req.get("product"))
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
        for p in products():
            if json.load(open(f"config/ads_{p}.json")).get("daily", True):
                run(f"daily-{p}-{today()}", {"op": "daily", "product": p})
        use_product()
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


# =====================================================================================
# v1.1: tactics (warm-up, reminder, unreachable), planner budgets, creative tester, lead join from the Lambda
# =====================================================================================
import random, urllib.request

def perf_summary():
    """Aggregates from the WhatsApp Lambda (/perf/summary). Needs secrets PERF_URL and PERF_KEY. No phone numbers."""
    url, key = os.environ.get("PERF_URL"), os.environ.get("PERF_KEY")
    if not url or not key:
        return None
    try:
        req = urllib.request.Request(f"{url}?days=28", headers={"x-perf-key": key})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except Exception as e:
        print("perf summary unavailable:", e)
        return None

def current_plan():
    try:
        p = json.load(open("perf/plan.json"))
    except Exception:
        return None
    if p.get("status") != "ok" or (today() - datetime.date.fromisoformat(p["date"])).days > 8:
        return None
    return p

def find_campaign_named(name):
    r = call(f"{ACT}/campaigns", {"fields": "id,name,status,effective_status", "limit": 100})
    return next((c for c in r.get("data", []) if c["name"] == name), None)

def fit_month_spend():
    tot = 0.0
    for n in (CFG["campaign_name"], CFG.get("warm_campaign_name", "")):
        c = find_campaign_named(n) if n else None
        if c:
            tot += spend(c["id"], "this_month")
    return tot

def tactic_audiences(key, summary, have):
    """Audience ids a tactic should target today, from the joint-wave schedule and the nightly lists."""
    t = CFG["tactics"][key]
    names = list(t.get("audiences", []))
    win = t.get("audience_window")
    if win and summary:
        lead = int((summary.get("perf") or {}).get("warm", {}).get("leadDays", 4))
        remind = int((summary.get("perf") or {}).get("warm", {}).get("remindDays", 10))
        for w in summary.get("schedule", []):
            d0 = datetime.date.fromisoformat(w["d0"])
            if win == "warm" and d0 - datetime.timedelta(days=lead) <= today() < d0:
                names.append(w["audience"])
            if win == "remind" and d0 <= today() < d0 + datetime.timedelta(days=remind):
                names.append(w["audience"])
    return [have[n] for n in names if n in have]

def op_tactics_setup(req):
    """Creates the reminder and unreachable ad sets (main campaign) and the warm-up campaign and ad set, all PAUSED."""
    st = load_state()
    p = ty_page()
    camp = find_campaign()
    if not camp:
        return {"error": "run setup first"}
    out = {}
    warm = find_campaign_named(CFG["warm_campaign_name"])
    if not warm:
        warm = call(f"{ACT}/campaigns", {"name": CFG["warm_campaign_name"], "objective": "OUTCOME_AWARENESS", "status": "PAUSED",
                    "special_ad_categories": CFG["special_ad_categories"], "is_adset_budget_sharing_enabled": "false",
                    "spend_cap": paise(CFG["monthly_cap_inr"])}, "POST")
        if "id" not in warm:
            return {"warm_campaign_error": err(warm)}
    out["warm_campaign"] = warm["id"]
    src_ads = {a["key"]: a["ads"] + a.get("video_ads", []) for a in CFG["adsets"]}
    existing = {s["name"]: s for s in adsets_of(camp["id"]) + adsets_of(warm["id"])}
    base_t = {"age_min": 25, "age_max": 65, "geo_locations": {"countries": ["IN"]}, "publisher_platforms": ["facebook", "instagram"],
              "targeting_automation": {"advantage_audience": 0}}
    for key, t in CFG["tactics"].items():
        if t["name"] in existing:
            st["adsets"][key] = existing[t["name"]]["id"]
            if not req.get("refresh_ads"):
                continue
            s = existing[t["name"]]; out[key] = {"adset": {"id": s["id"]}, "deleted": []}
            for a in ads_of(warm["id"] if t["kind"] == "photo" else camp["id"]):
                if a["adset_id"] == s["id"]:
                    call(a["id"], {"status": "DELETED"}, "POST"); out[key]["deleted"].append(a["name"])
        else:
            if t["kind"] == "photo":
                s = call(f"{ACT}/adsets", {"name": t["name"], "campaign_id": warm["id"], "status": "PAUSED", "daily_budget": paise(CFG["min_adset_daily_inr"]),
                         "billing_event": "IMPRESSIONS", "optimization_goal": "REACH", "bid_strategy": "LOWEST_COST_WITHOUT_CAP", "targeting": base_t,
                         "frequency_control_specs": [{"event": "IMPRESSIONS", "interval_days": 7, "max_frequency": t.get("max_frequency_7d", 3)}]}, "POST")
            else:
                s = call(f"{ACT}/adsets", {"name": t["name"], "campaign_id": camp["id"], "status": "PAUSED", "daily_budget": paise(CFG["min_adset_daily_inr"]),
                         "billing_event": "IMPRESSIONS", "optimization_goal": "CONVERSATIONS", "destination_type": "WHATSAPP",
                         "bid_strategy": "LOWEST_COST_WITHOUT_CAP", "targeting": base_t, "promoted_object": {"page_id": p["id"]}}, "POST")
            out[key] = {"adset": s}
            if "id" not in s:
                continue
        st["adsets"][key] = s["id"]
        for ad in src_ads.get(t["ads_from"], []):
            ad2 = dict(ad, name=key + ad["name"][1:])
            try:
                if t["kind"] == "photo" and "video" in ad2:
                    vid = upload_video(ad2["video"]); th = upload_image(ad2["thumb"])
                    cr = call(f"{ACT}/adcreatives", {"name": f"FIT {ad2['name']}", "object_story_spec": {"page_id": p["id"], "instagram_user_id": CFG["instagram_user_id"],
                              "video_data": {"video_id": vid, "image_hash": th, "message": ad2["text"], "title": ad2["headline"]}},
                              **({"degrees_of_freedom_spec": opt_out_spec()} if opt_out_spec() else {})}, "POST")
                    r = call(f"{ACT}/ads", {"name": ad2["name"], "adset_id": s["id"], "creative": {"creative_id": cr.get("id")}, "status": "PAUSED"}, "POST") if "id" in cr else {"error": err(cr)}
                elif "video" in ad2:
                    r = make_video_ad(p["id"], s["id"], ad2, "PAUSED")
                elif t["kind"] == "photo":
                    h = upload_image(ad2["image"])
                    cr = call(f"{ACT}/adcreatives", {"name": f"FIT {ad2['name']}", "object_story_spec": {"page_id": p["id"], "instagram_user_id": CFG["instagram_user_id"],
                              "photo_data": {"image_hash": h, "caption": ad2["text"]}}}, "POST")
                    r = call(f"{ACT}/ads", {"name": ad2["name"], "adset_id": s["id"], "creative": {"creative_id": cr.get("id")}, "status": "PAUSED"}, "POST") if "id" in cr else {"error": err(cr)}
                else:
                    r = make_ad(p["id"], s["id"], ad2, "PAUSED")
            except Exception as e:
                r = {"error": str(e)}
            out[key][ad2["name"]] = r
    save_state(st)
    return out

def meta_ramp(rep, base, dry):
    """Extra Meta budget on top of the planner's share, stepped toward target_inr (Rishi's go-ahead, 18 Nov 2026).
    No fixed cost threshold (Rishi, 20 Nov 2026: "don't add checks like that, do what is optimal"). The ramp follows
    returns instead: it measures cost per qualified lead (cost per chat until there are qualified leads) and compares it
    with the value it had at the last step. Step up step_pct every min_days while that cost has not risen by more than
    25% (more money is still buying leads at about the same price) and Meta spent at least min_delivery of the budget;
    step back step_pct (never below the planner's share) when it has risen by more than 50%; otherwise hold.
    The daily and monthly caps still apply above this."""
    R = CFG.get("meta_ramp")
    if not R:
        return 0.0
    st = load_state(); r = st.get("meta_ramp") or {"level": base, "at": None}
    level = float(r.get("level") or base)
    ads = rep.get("ads") or []
    sp = sum(a.get("spend_life") or 0 for a in ads); q = sum(a.get("qualified") or 0 for a in ads)
    ch = sum(a.get("conv_life") or 0 for a in ads)
    metric, cost = ("qualified lead", round(sp / q)) if q else (("chat", round(sp / ch)) if ch else (None, None))
    ref = r.get("ref") if r.get("ref_metric") == metric else None
    why = "held"
    if str(today()) >= R.get("start_on", ""):
        days = (today() - datetime.date.fromisoformat(r["at"])).days if r.get("at") else 99
        deliv = (rep.get("spend_yesterday_inr") or 0) / max(1.0, rep.get("daily_budget_total_inr") or 1)
        new = level
        if cost is None:
            why = "held: no chats yet"
        elif days < R["min_days"]:
            why = f"next review after {R['min_days'] - days} more day(s)"
        elif ref and cost > ref * 1.5 and level > base:
            new = max(base, round(level / (1 + R["step_pct"] / 100))); why = f"stepped back: cost per {metric} INR {cost}, was INR {ref} at the last step"
        elif level >= R["target_inr"]:
            why = "at target"
        elif deliv < R["min_delivery"]:
            why = f"held: Meta spent only {deliv:.0%} of the budget"
        elif ref and cost > ref * 1.25:
            why = f"held: cost per {metric} INR {cost}, up from INR {ref} at the last step"
        else:
            new = min(R["target_inr"], round(level * (1 + R["step_pct"] / 100))); why = "stepped up"
        if new != level:
            rep["actions"].append(f"Meta ramp: INR {level:.0f} -> {new}/day (cost per {metric} INR {cost}" + (f", INR {ref} at the last step" if ref else "") + f", delivery {deliv:.0%})")
            level = new
            if not dry:
                st["meta_ramp"] = {"level": level, "at": str(today()), "ref": cost, "ref_metric": metric}; save_state(st)
        elif not dry and cost is not None and not ref:
            st["meta_ramp"] = {**r, "level": level, "ref": cost, "ref_metric": metric}; save_state(st)
    rep["meta_ramp"] = f"Meta ramp: INR {level:.0f}/day toward {R['target_inr']} ({why})"
    return max(0.0, level - base)

def apply_tactics_and_plan(rep, summary, dry):
    """Daily: point each tactic at today's audiences (pause it when there are none) and set budgets from the planner.
    The sum never exceeds daily_cap_inr; idle tactic money goes to prospecting; nothing goes live without approval."""
    camp = find_campaign()
    warm = find_campaign_named(CFG.get("warm_campaign_name", ""))
    sets = {s["name"]: s for s in (adsets_of(camp["id"]) if camp else []) + (adsets_of(warm["id"]) if warm else [])}
    have = {a["name"]: a["id"] for a in call(f"{ACT}/customaudiences", {"fields": "id,name", "limit": 500}).get("data", [])}
    excl = [{"id": have[n]} for n in CFG.get("exclude_audience_names", []) if n in have]
    live_main = live_ok() and camp and camp.get("status") == "ACTIVE"
    live_warm = live_main and CFG.get("warm_launch_approved") and warm
    active_tactics = {}
    for key, t in CFG.get("tactics", {}).items():
        s = sets.get(t["name"])
        if not s:
            continue
        ids = tactic_audiences(key, summary, have)
        allowed = live_warm if t["campaign"] == "warm" else live_main
        if ids and allowed:
            tg = {"age_min": 25, "age_max": 65, "geo_locations": {"countries": ["IN"]}, "publisher_platforms": ["facebook", "instagram"],
                  "targeting_automation": {"advantage_audience": 0}, "custom_audiences": [{"id": i} for i in ids], "excluded_custom_audiences": excl}
            active_tactics[key] = s
            if not dry:
                call(s["id"], {"targeting": tg, "status": "ACTIVE"}, "POST")
                for a in ads_of(warm["id"] if t["campaign"] == "warm" else camp["id"]):
                    if a["adset_id"] == s["id"] and a["status"] == "PAUSED" and a["name"] not in load_state().get("tester_paused", []):
                        call(a["id"], {"status": "ACTIVE"}, "POST")
            rep["actions"].append(f"{t['name']}: targeting {len(ids)} audience(s)")
        elif s["status"] == "ACTIVE":
            if not dry:
                call(s["id"], {"status": "PAUSED"}, "POST")
            rep["actions"].append(f"Paused {t['name']}: {'no audiences in its window today' if not ids else 'not approved'}")
    plan = current_plan()
    if not plan or not live_main:
        rep["plan"] = "no current plan (planner awaiting total)" if not plan else "plan waiting for launch approval"
        return
    meta = min(float(plan["meta_budget_inr"]) + meta_ramp(rep, float(plan["meta_budget_inr"]), dry), float(CFG["daily_cap_inr"]))
    tb = plan["meta_tactics"]
    want = {k: float(tb.get({"W": "warm", "R": "remind", "U": "unreach"}[k], 0)) for k in active_tactics}
    idle = sum(float(tb.get(x, 0)) for k, x in (("W", "warm"), ("R", "remind"), ("U", "unreach")) if k not in active_tactics)
    prospect = max(0.0, meta - sum(want.values()))
    pa = [sets[a["name"]] for a in CFG["adsets"] if a["key"] in ("A", "B", "P") and a["name"] in sets and sets[a["name"]]["status"] == "ACTIVE"]
    cur = sum(inr(s["daily_budget"]) for s in pa) or 1
    for s in pa:
        want[s["name"]] = prospect * inr(s["daily_budget"]) / cur
    floor = CFG["min_adset_daily_inr"]
    total = 0
    for k, v in want.items():
        s = active_tactics.get(k) or sets.get(k)
        nb = max(floor, int(v))
        total += nb
        if abs(nb - inr(s.get("daily_budget", 0))) >= 10:
            rep["actions"].append(f"Budget {s['name']}: INR {inr(s.get('daily_budget', 0)):.0f} -> {nb} (planner)")
            if not dry and total <= CFG["daily_cap_inr"]:
                call(s["id"], {"daily_budget": paise(nb)}, "POST")
    rep["plan"] = f"planner {plan['date']}: Meta INR {meta:.0f}/day ({'idle tactics folded into prospecting: INR %d' % idle if idle else 'all tactics active'})"

def creative_tester(rep, life, leads, dry):
    """Thompson sampling per ad set: results per rupee (qualified leads when the join exists, else chats).
    Pause an ad once it has had a fair spend and under 5% chance of being the best; keep at least one ad running."""
    T = CFG.get("tester", {})
    if today().weekday() != T.get("batch_weekday", 0) and not CFG.get("_tester_force"):
        rep["tester"] = "waits for the weekly batch (Monday): edits reset Meta's learning"
        return
    st = load_state()
    paused = set(st.get("tester_paused", []))
    by_set = {}
    for camp_name in (CFG["campaign_name"], CFG.get("warm_campaign_name", "")):
        c = find_campaign_named(camp_name) if camp_name else None
        if c:
            for a in ads_of(c["id"]):
                if a["status"] == "ACTIVE":
                    by_set.setdefault(a["adset_id"], []).append(a)
    prior = float(CFG["target_cost_per_conversation_inr"]) if leads is None else float(CFG["target_cost_per_qualified_lead_inr"])
    ledger = {}
    for sid, ads in by_set.items():
        rows = []
        for a in ads:
            L = life.get(a["id"], {})
            res = ((leads or {}).get(a["id"], {}).get("qualified") or 0) if leads is not None else L.get("conversations", 0)
            rows.append((a, L.get("spend", 0.0), res))
            ledger[a["name"]] = {"spend": round(L.get("spend", 0.0)), "results": res, "metric": "qualified" if leads is not None else "chats"}
        if len(rows) < 2:
            continue
        rng = random.Random(f"{today()}{sid}")
        wins = {a["id"]: 0 for a, _, _ in rows}
        for _ in range(int(T.get("draws", 4000))):
            best = max(rows, key=lambda r: rng.gammavariate(r[2] + 1, 1.0 / (r[1] + prior)))
            wins[best[0]["id"]] += 1
        pb = {k: v / T.get("draws", 4000) for k, v in wins.items()}
        done = {x.split(":")[0].replace("PAUSED ad ", "") for x in rep["actions"] if x.startswith("PAUSED ad ")}
        for a, sp, res in sorted(rows, key=lambda r: pb[r[0]["id"]]):
            ledger[a["name"]]["p_best"] = round(pb[a["id"]], 3)
            if a["name"] in done:
                a["status"] = "PAUSED"; continue
            active_left = sum(1 for r in rows if r[0]["status"] == "ACTIVE")
            zero_rule = leads is not None and sp >= T.get("min_spend_inr", 800) and res == 0
            post_rule = sp >= T.get("posterior_spend_inr", 3000) and pb[a["id"]] < T.get("p_best_floor", 0.10)
            if (zero_rule or post_rule) and active_left > T.get("min_active_ads", 4):
                rep["actions"].append(f"Tester paused {a['name']}: {pb[a['id']]:.0%} chance of being best after INR {sp:.0f} ({res} results)")
                a["status"] = "PAUSED"; paused.add(a["name"])
                if not dry:
                    call(a["id"], {"status": "PAUSED"}, "POST")
        if sum(1 for r in rows if r[0]["status"] == "ACTIVE") < T.get("min_active_ads", 2):
            rep["flags"].append(f"Ad set {sid}: under {T.get('min_active_ads', 2)} active ads, make fresh creatives (angles that won: see perf/creatives.json)")
    if not dry:
        st["tester_paused"] = sorted(paused); save_state(st)
        os.makedirs("perf", exist_ok=True)
        hist = {}
        try:
            hist = json.load(open("perf/creatives.json"))
        except Exception:
            pass
        hist.update({k: {**hist.get(k, {}), **v, "updated": str(today())} for k, v in ledger.items()})
        json.dump(hist, open("perf/creatives.json", "w"), indent=1, sort_keys=True)
    rep["tester"] = ledger

OPS["tactics_setup"] = op_tactics_setup

def op_plan(req):
    """Run the media planner now (it also runs Mondays 06:30 IST)."""
    import perf_planner
    return perf_planner.plan()
OPS["plan"] = op_plan

# ---------- video ads (Reels and Stories, 9:16) ----------
RAW = "https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/"

def upload_video(path, wait_s=300):
    r = call(f"{ACT}/advideos", {"file_url": RAW + path, "name": os.path.basename(path)}, "POST")
    if "id" not in r:
        raise RuntimeError(f"video upload failed for {path}: {err(r)}")
    vid, t0 = r["id"], time.time()
    while time.time() - t0 < wait_s:
        st = call(vid, {"fields": "status"}).get("status", {})
        if st.get("video_status") == "ready":
            return vid
        if st.get("video_status") == "error":
            raise RuntimeError(f"video processing failed: {st}")
        time.sleep(10)
    return vid  # still processing; Meta accepts the creative once it is ready

def make_video_ad(page_id, adset_id, ad, status):
    vid = upload_video(ad["video"])
    thumb = upload_image(ad["thumb"])
    vd = {"video_id": vid, "image_hash": thumb, "message": ad["text"], "title": ad["headline"],
          "call_to_action": {"type": "WHATSAPP_MESSAGE", "value": {"app_destination": "WHATSAPP"}}}
    spec = {"page_id": page_id, "video_data": vd}
    if CFG.get("instagram_user_id"):
        spec["instagram_user_id"] = CFG["instagram_user_id"]
    cr, errs, notes = create_creative(f"FIT {ad['name']}", spec, "video_data", ad)
    if "id" not in cr:
        return {"error": errs}
    a = call(f"{ACT}/ads", {"name": ad["name"], "adset_id": adset_id, "creative": {"creative_id": cr["id"]}, "status": status}, "POST")
    return {"ad": a, "creative_id": cr["id"], "video_id": vid, "creative_notes": notes, "earlier_errors": errs}

def op_add_video_ads(req):
    """{"adset_key": "A", "ads": [{video, thumb, name, headline, text}]}. Paused unless the campaign is live and approved."""
    camp, st = find_campaign(), load_state()
    sid = st.get("adsets", {}).get(req["adset_key"])
    if not camp or not sid:
        return {"error": "campaign or ad set missing, run setup"}
    have = {a["name"] for a in ads_of(camp["id"])}
    status = "ACTIVE" if (live_ok() and camp.get("status") == "ACTIVE") else "PAUSED"
    p, out = ty_page(), {}
    for ad in req["ads"]:
        if ad["name"] in have:
            out[ad["name"]] = "exists"; continue
        try:
            r = make_video_ad(p["id"], sid, ad, status)
        except Exception as e:
            r = {"error": str(e)}
        out[ad["name"]] = r
        if "ad" in r and "id" in r["ad"]:
            st["ads"][ad["name"]] = r["ad"]["id"]
    save_state(st)
    return {"status_used": status, "ads": out}
OPS["add_video_ads"] = op_add_video_ads


def op_rebuild_ads(req):
    """Delete and recreate the current campaign's ads (only while the campaign is PAUSED). Use after creative-spec changes."""
    camp = find_campaign()
    if not camp:
        return {"error": "run setup first"}
    if camp.get("status") != "PAUSED":
        return {"blocked": "campaign is live; rebuild only applies to a paused campaign"}
    gone = []
    for a in ads_of(camp["id"]):
        call(a["id"], {"status": "DELETED"}, "POST"); gone.append(a["name"])
    st = load_state(); st["ads"] = {k: v for k, v in st.get("ads", {}).items() if k not in gone}; save_state(st)
    return {"deleted": gone, "setup": op_setup(req)}
OPS["rebuild_ads"] = op_rebuild_ads


def op_archive_legacy(req):
    """Archive the old v1 campaign (paused, never launched) so only the current campaign remains."""
    name = CFG.get("legacy_campaign_name")
    c = find_campaign_named(name) if name else None
    if not c:
        return {"note": "no legacy campaign"}
    if c.get("status") == "ACTIVE":
        return {"blocked": "legacy campaign is active; pause it first"}
    return {"campaign": name, "result": call(c["id"], {"status": "ARCHIVED"}, "POST")}
OPS["archive_legacy"] = op_archive_legacy


def op_delete_paused(req):
    """{"ids": [...]} Delete ad sets or ads by id, only if they are PAUSED (cleanup of duplicates)."""
    out = {}
    for i in req.get("ids", []):
        o = call(i, {"fields": "name,status"})
        if o.get("status") != "PAUSED":
            out[i] = {"skipped": o}; continue
        out[i] = {"name": o.get("name"), "result": call(i, {"status": "DELETED"}, "POST")}
    return out
OPS["delete_paused"] = op_delete_paused


def op_set_budget(req):
    """Changes the daily budget of existing ad sets to match the config (adsets[].daily_budget_inr), within the daily cap.
    Request: {"op": "set_budget", "product": "jind"}. Only lowers or raises to what the config already says."""
    camp = find_campaign()
    if not camp:
        return {"error": "no campaign"}
    enabled = [a for a in CFG["adsets"] if a.get("enabled")]
    total = sum(a["daily_budget_inr"] for a in enabled)
    if total > CFG["daily_cap_inr"]:
        return {"blocked": f"budgets INR {total} above daily cap INR {CFG['daily_cap_inr']}"}
    want = {a["name"]: a["daily_budget_inr"] for a in enabled}
    out = {}
    for s_ in adsets_of(camp["id"]):
        if s_["name"] in want and inr(s_["daily_budget"]) != want[s_["name"]]:
            out[s_["name"]] = call(s_["id"], {"daily_budget": paise(want[s_["name"]])}, "POST")
    return out or {"note": "budgets already match the config"}
OPS["set_budget"] = op_set_budget


if __name__ == "__main__":
    main()
