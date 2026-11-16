#!/usr/bin/env python3
"""TrueYards Meta autopilot. Reads meta/requests/*.json, writes meta/results/<name>.json.
The token comes from the META_TOKEN secret and is never written or printed.
Spend rules (learnings/BOOST_POLICY.md) are enforced here, not just in prompts."""
import json, os, sys, glob, time, urllib.request, urllib.parse, urllib.error, datetime

V = "v23.0"
G = f"https://graph.facebook.com/{V}"
TOKEN = os.environ.get("META_TOKEN", "")
CFG = json.load(open("config/meta.json"))
ACT = CFG["ad_account_id"]

def scrub(o):
    if isinstance(o, dict):
        return {k: scrub(v) for k, v in o.items() if k != "access_token"}
    if isinstance(o, list):
        return [scrub(x) for x in o]
    if isinstance(o, str) and TOKEN and TOKEN in o:
        return o.replace(TOKEN, "***")
    return o

def call(path, params=None, method="GET", token=None):
    p = dict(params or {})
    p["access_token"] = token or TOKEN
    data = None
    url = f"{G}/{path.lstrip('/')}"
    if method == "GET":
        url += "?" + urllib.parse.urlencode(p)
    else:
        data = urllib.parse.urlencode({k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in p.items()}).encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return {"error": json.loads(e.read()).get("error")}
        except Exception:
            return {"error": {"message": f"HTTP {e.code}"}}

def page():
    r = call("me/accounts", {"fields": "id,name,access_token,instagram_business_account"})
    for p in r.get("data", []):
        return p
    return None

# ---------- read ops ----------
def op_test(req):
    out = {"me": call("me", {"fields": "id,name"}),
           "permissions": call("me/permissions")}
    p = page()
    out["page"] = scrub(p) if p else {"error": "no page visible to the bot"}
    out["ad_account"] = call(ACT, {"fields": "name,account_status,currency,timezone_name,amount_spent,balance,spend_cap,disable_reason"})
    out["instagram"] = call(CFG["ig_user_id"], {"fields": "username,followers_count,media_count"})
    return out

def op_insights(req):
    days = int(req.get("days", 30))
    ig = CFG["ig_user_id"]
    since = int(time.time()) - days * 86400
    media, url = [], f"{ig}/media"
    params = {"fields": "id,permalink,media_type,media_product_type,timestamp,caption,like_count,comments_count", "limit": 50}
    r = call(url, params)
    while True:
        for m in r.get("data", []):
            ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z").timestamp()
            if ts < since:
                r = {}
                break
            reel = m.get("media_product_type") == "REELS"
            want = ["reach", "views", "likes", "comments", "shares", "saved", "total_interactions", "follows", "profile_visits"]
            if reel:
                want += ["ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate"]
            got, errs = {}, {}
            ins = call(f"{m['id']}/insights", {"metric": ",".join(want)})
            if "error" in ins:
                for w in want:
                    one = call(f"{m['id']}/insights", {"metric": w})
                    if "error" in one:
                        errs[w] = one["error"].get("message", "")[:80]
                    for d in one.get("data", []):
                        got[d["name"]] = d["values"][0]["value"] if d.get("values") else d.get("total_value", {}).get("value")
            else:
                for d in ins.get("data", []):
                    got[d["name"]] = d["values"][0]["value"] if d.get("values") else d.get("total_value", {}).get("value")
            m["insights"] = got
            if errs:
                m["unavailable_metrics"] = errs
            media.append(m)
        nxt = r.get("paging", {}).get("next") if r else None
        if not nxt:
            break
        with urllib.request.urlopen(nxt, timeout=60) as h:
            r = json.loads(h.read())
    acct = {
        "profile": call(ig, {"fields": "username,followers_count,media_count"}),
        "daily": call(f"{ig}/insights", {"metric": "reach,follower_count", "period": "day", "since": max(since, int(time.time()) - 29 * 86400), "until": int(time.time())}),
        "nonfollower_reach": call(f"{ig}/insights", {"metric": "reach", "period": "day", "metric_type": "total_value", "breakdown": "follow_type", "since": int(time.time()) - 7 * 86400, "until": int(time.time())}),
    }
    p = page()
    fb = {}
    if p:
        fb = {"page": call(p["id"], {"fields": "name,followers_count,fan_count"}, token=p["access_token"]),
              "insights": call(f"{p['id']}/insights", {"metric": "page_impressions_unique,page_post_engagements,page_daily_follows_unique", "period": "day", "date_preset": "last_28d"}, token=p["access_token"])}
    return scrub({"instagram_media": media, "instagram_account": acct, "facebook": fb})

def month_spend():
    r = call(f"{ACT}/insights", {"fields": "spend", "date_preset": "this_month"})
    d = r.get("data", [])
    return float(d[0]["spend"]) if d else 0.0

def op_boost_status(req):
    camps = call(f"{ACT}/campaigns", {"fields": "id,name,status,effective_status,daily_budget", "limit": 50})
    ads = call(f"{ACT}/ads", {"fields": "id,name,status,effective_status,creative{object_story_id,source_instagram_media_id}", "limit": 100})
    ins = call(f"{ACT}/insights", {"level": "ad", "fields": "ad_id,ad_name,spend,impressions,reach,actions,cost_per_action_type", "date_preset": "last_7d"})
    return {"month_spend_inr": month_spend(), "campaigns": camps, "ads": ads, "insights_7d": ins}

# ---------- spend ops (guarded) ----------
BOOST_NAME = "TrueYards Boost"

def guard():
    cap = float(CFG["boost_monthly_cap_inr"])
    spent = month_spend()
    if spent + float(CFG["boost_daily_budget_inr"]) > cap:
        raise SystemExit(f"monthly cap reached: spent INR {spent:.0f} of {cap:.0f}")
    return spent

def find_campaign():
    r = call(f"{ACT}/campaigns", {"fields": "id,name,status,daily_budget", "limit": 50})
    for c in r.get("data", []):
        if c["name"] == BOOST_NAME:
            return c
    return None

def make_adset(camp_id):
    base = {"campaign_id": camp_id, "status": "PAUSED", "billing_event": "IMPRESSIONS",
            "targeting": {"geo_locations": {"countries": ["IN"]}, "age_min": 22,
                          "publisher_platforms": ["instagram", "facebook"],
                          "targeting_automation": {"advantage_audience": 1}}}
    tries = [
        dict(name="TrueYards Boost - India profile visits", optimization_goal="PROFILE_AND_PAGE_ENGAGEMENT",
             destination_type="INSTAGRAM_PROFILE"),
        dict(name="TrueYards Boost - India engagement", optimization_goal="POST_ENGAGEMENT", destination_type="ON_POST"),
    ]
    errs = []
    for t in tries:
        r = call(f"{ACT}/adsets", {**base, **t}, "POST")
        if "id" in r:
            return {"adset": r, "goal": t["optimization_goal"], "earlier_errors": errs}
        errs.append(r.get("error", {}).get("error_user_msg") or r.get("error", {}).get("message"))
        if "regional" in json.dumps(r).lower():
            base["regional_regulated_categories"] = []
    return {"error": errs}

def op_boost_setup(req):
    """One-time: creates the single always-on campaign + ad set, PAUSED. Budget fixed from config."""
    c = find_campaign()
    if not c:
        budget = int(CFG["boost_daily_budget_inr"]) * 100  # paise
        c = call(f"{ACT}/campaigns", {"name": BOOST_NAME, "objective": "OUTCOME_ENGAGEMENT", "status": "PAUSED",
                 "special_ad_categories": [], "daily_budget": budget, "bid_strategy": "LOWEST_COST_WITHOUT_CAP"}, "POST")
        if "error" in c:
            return {"campaign_error": c}
    sets = call(f"{c['id']}/adsets", {"fields": "id,name,optimization_goal,status"}).get("data", [])
    if sets:
        return {"campaign": c, "adsets": sets, "note": "already set up"}
    return {"campaign": c, **make_adset(c["id"])}

def op_boost_post(req):
    """Adds an existing Instagram post as an ad inside the fixed campaign. Never touches budget."""
    guard()
    camp = find_campaign()
    if not camp:
        return {"error": "run boost_setup first"}
    sets = call(f"{camp['id']}/adsets", {"fields": "id,name"}).get("data", [])
    if not sets:
        return {"error": "no ad set"}
    p = page()
    creative = call(f"{ACT}/adcreatives", {"name": f"boost {req['media_id']}", "object_id": p["id"],
                    "instagram_user_id": CFG["ig_user_id"], "source_instagram_media_id": req["media_id"],
                    }, "POST")
    if "error" in creative:
        return {"creative_error": creative}
    ad = call(f"{ACT}/ads", {"name": f"boost {req['media_id']}", "adset_id": sets[0]["id"],
              "creative": {"creative_id": creative["id"]}, "status": "ACTIVE"}, "POST")
    on = {}
    if req.get("activate", True):
        on["adset"] = call(sets[0]["id"], {"status": "ACTIVE"}, "POST")
        on["campaign"] = call(camp["id"], {"status": "ACTIVE"}, "POST")
    return {"creative": creative, "ad": ad, "activated": on}

def op_pause_ad(req):
    return call(req["ad_id"], {"status": "PAUSED"}, "POST")

def op_pause_all(req):
    camp = find_campaign()
    return call(camp["id"], {"status": "PAUSED"}, "POST") if camp else {"note": "no campaign"}

OPS = {"test": op_test, "insights": op_insights, "boost_status": op_boost_status,
       "boost_setup": op_boost_setup, "boost_post": op_boost_post, "pause_ad": op_pause_ad, "pause_all": op_pause_all}
# Deliberately absent: any op that changes budget, billing or creates other campaigns.

def main():
    if not TOKEN:
        sys.exit("META_TOKEN secret missing")
    os.makedirs("meta/results", exist_ok=True)
    for f in sorted(glob.glob("meta/requests/*.json")):
        name = os.path.basename(f)[:-5]
        try:
            req = json.load(open(f))
            fn = OPS.get(req.get("op"))
            res = fn(req) if fn else {"error": f"unknown op {req.get('op')}"}
        except SystemExit as e:
            res = {"blocked": str(e)}
        except Exception as e:
            res = {"error": f"{type(e).__name__}: {e}"}
        res = scrub({"op": req.get("op") if isinstance(req, dict) else None, "ran_at": datetime.datetime.utcnow().isoformat() + "Z", "result": res})
        json.dump(res, open(f"meta/results/{name}.json", "w"), indent=1)
        os.remove(f)
        print(f"done {name}")

if __name__ == "__main__":
    main()
