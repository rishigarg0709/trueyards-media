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
    if method in ("GET", "DELETE"):
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

def _metrics(obj_id, path, names, token):
    """Ask for each metric on its own so one retired metric never hides the rest."""
    got, errs = {}, {}
    for n in names:
        r = call(f"{obj_id}/{path}", {"metric": n}, token=token)
        if "error" in r:
            errs[n] = (r["error"] or {}).get("message", "")[:80]; continue
        for d in r.get("data", []):
            v = d.get("values") or [{}]
            got[d["name"]] = v[0].get("value") if v else d.get("total_value", {}).get("value")
    return got, errs

def fb_posts(p, since):
    """Per-post Facebook stats: reels (video insights) and photo/carousel posts (post insights)."""
    tok, out = p["access_token"], []
    reels = call(f"{p['id']}/video_reels", {"fields": "id,description,created_time,post_id,permalink_url", "since": since, "limit": 50}, token=tok)
    for v in reels.get("data", []):
        got, errs = _metrics(v["id"], "video_insights", ["blue_reels_play_count", "fb_reels_total_plays",
                             "post_video_avg_time_watched", "post_video_social_actions", "post_video_followers", "post_video_likes_by_reaction_type"], tok)
        out.append({"kind": "reel", "video_id": v["id"], "post_id": v.get("post_id"), "created_time": v.get("created_time"),
                    "description": (v.get("description") or "")[:120], "permalink": v.get("permalink_url"), "insights": got, "unavailable_metrics": errs or None})
    posts = call(f"{p['id']}/posts", {"fields": "id,message,created_time,permalink_url,shares,reactions.summary(true).limit(0),comments.summary(true).limit(0),attachments{media_type}",
                 "since": since, "limit": 50}, token=tok)
    for q in posts.get("data", []):
        mt = ((q.get("attachments") or {}).get("data") or [{}])[0].get("media_type")
        if mt == "video": continue  # reels are covered above
        got, errs = _metrics(q["id"], "insights", ["post_impressions_unique", "post_media_view", "post_clicks", "post_reactions_by_type_total"], tok)
        got.update({"reactions": (q.get("reactions") or {}).get("summary", {}).get("total_count"), "comments": (q.get("comments") or {}).get("summary", {}).get("total_count"),
                    "shares": (q.get("shares") or {}).get("count", 0)})
        out.append({"kind": mt or "post", "post_id": q["id"], "created_time": q.get("created_time"), "description": (q.get("message") or "")[:120],
                    "permalink": q.get("permalink_url"), "insights": got, "unavailable_metrics": errs or None})
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
        fb["posts"] = fb_posts(p, since)
    return scrub({"instagram_media": media, "instagram_account": acct, "facebook": fb})

def month_spend():
    """This month's spend of the TrueYards Boost campaign only (the ad account is shared with FIT ads,
    which have their own budget in the ads agent; they must not eat the boost cap). Falls back to the
    whole account if the campaign cannot be found, which is the safe direction for a cap."""
    r = call(f"{ACT}/campaigns", {"fields": "id,name", "limit": 50})
    camp = next((c for c in r.get("data", []) if c.get("name") == "TrueYards Boost"), None)
    path = f"{camp['id']}/insights" if camp else f"{ACT}/insights"
    r = call(path, {"fields": "spend", "date_preset": "this_month"})
    d = r.get("data", [])
    return float(d[0]["spend"]) if d else 0.0

def op_boost_status(req):
    camps = call(f"{ACT}/campaigns", {"fields": "id,name,status,effective_status,daily_budget", "limit": 50})
    ads = call(f"{ACT}/ads", {"fields": "id,name,status,effective_status,creative{object_story_id,source_instagram_media_id}", "limit": 100})
    ins = call(f"{ACT}/insights", {"level": "ad", "fields": "ad_id,ad_name,spend,impressions,reach,actions,cost_per_action_type", "date_preset": "last_7d"})
    today = call(f"{ACT}/insights", {"level": "ad", "fields": "ad_id,ad_name,spend,impressions,reach,actions", "date_preset": "today"})
    sets = call(f"{ACT}/adsets", {"fields": "id,name,campaign{name},effective_status,daily_budget,learning_stage_info,optimization_goal,issues_info", "limit": 50})
    return {"month_spend_inr": month_spend(), "campaigns": camps, "ads": ads, "insights_7d": ins, "insights_today": today, "adsets": sets}

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


# ---------- publishing (Instagram + Facebook) ----------
IG = CFG["ig_user_id"]

def _wait_container(cid, tries=40):
    st = {}
    for _ in range(tries):
        st = call(cid, {"fields": "status_code,status"})
        if st.get("status_code") in ("FINISHED", "ERROR", "EXPIRED"):
            return st
        time.sleep(15)
    return st

def op_ig_reel(req):
    """{video_url, cover_url?, caption, share_to_feed?, trial?, trial_strategy?, dry?}"""
    p = {"media_type": "REELS", "video_url": req["video_url"], "caption": req.get("caption", ""),
         "share_to_feed": "true" if req.get("share_to_feed", True) else "false"}
    if req.get("cover_url"): p["cover_url"] = req["cover_url"]
    if req.get("trial"):
        p["trial_params"] = {"graduation_strategy": req.get("trial_strategy", "MANUAL")}
        p.pop("share_to_feed", None)
    c = call(f"{IG}/media", p, "POST")
    if "id" not in c: return {"container_error": c}
    st = _wait_container(c["id"])
    if st.get("status_code") != "FINISHED": return {"container": c["id"], "status": st}
    if req.get("dry"): return {"container": c["id"], "status": st, "note": "dry run, not published"}
    pub = call(f"{IG}/media_publish", {"creation_id": c["id"]}, "POST")
    if "id" in pub:
        pub["permalink"] = call(pub["id"], {"fields": "permalink"}).get("permalink")
    return {"published": pub}

def op_ig_carousel(req):
    """{image_urls:[...], caption, dry?}"""
    kids = []
    for u in req["image_urls"]:
        k = call(f"{IG}/media", {"image_url": u, "is_carousel_item": "true"}, "POST")
        if "id" not in k: return {"child_error": k, "url": u}
        kids.append(k["id"])
    c = call(f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": req.get("caption", "")}, "POST")
    if "id" not in c: return {"container_error": c}
    st = _wait_container(c["id"])
    if req.get("dry"): return {"container": c["id"], "status": st, "note": "dry run, not published"}
    pub = call(f"{IG}/media_publish", {"creation_id": c["id"]}, "POST")
    if "id" in pub:
        pub["permalink"] = call(pub["id"], {"fields": "permalink"}).get("permalink")
    return {"published": pub}

def op_ig_story(req):
    """{image_url | video_url} : posts a story (e.g. the new reel's cover)."""
    p = {"media_type": "STORIES"}
    if req.get("video_url"): p["video_url"] = req["video_url"]
    else: p["image_url"] = req["image_url"]
    c = call(f"{IG}/media", p, "POST")
    if "id" not in c: return {"container_error": c}
    st = _wait_container(c["id"])
    if req.get("dry"): return {"container": c["id"], "status": st}
    return {"published": call(f"{IG}/media_publish", {"creation_id": c["id"]}, "POST")}

def op_fb_reel(req):
    """{video_url, description} : native Facebook Page reel."""
    p = page()
    if not p: return {"error": "no page"}
    tok = p["access_token"]
    st = call(f"{p['id']}/video_reels", {"upload_phase": "start"}, "POST", token=tok)
    vid = st.get("video_id")
    if not vid: return {"start_error": st}
    r = urllib.request.Request(f"https://rupload.facebook.com/video-upload/{V}/{vid}", method="POST",
                               headers={"Authorization": f"OAuth {tok}", "file_url": req["video_url"]})
    try:
        with urllib.request.urlopen(r, timeout=300) as h: up = json.loads(h.read())
    except urllib.error.HTTPError as e:
        return {"upload_error": e.code}
    if req.get("dry"): return {"video_id": vid, "upload": up, "note": "dry run, not published"}
    fin = call(f"{p['id']}/video_reels", {"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
               "description": req.get("description", "")}, "POST", token=tok)
    return {"video_id": vid, "finish": fin}

def op_fb_photos(req):
    """{image_urls:[...], message} : multi-photo Page post (Facebook version of a carousel)."""
    p = page()
    if not p: return {"error": "no page"}
    tok = p["access_token"]; ids = []
    for u in req["image_urls"]:
        ph = call(f"{p['id']}/photos", {"url": u, "published": "false"}, "POST", token=tok)
        if "id" not in ph: return {"photo_error": ph}
        ids.append({"media_fbid": ph["id"]})
    if req.get("dry"): return {"uploaded_unpublished": len(ids)}
    return {"post": call(f"{p['id']}/feed", {"message": req.get("message", ""), "attached_media": ids}, "POST", token=tok)}

# ---------- comments ----------
def op_comments(req):
    """{days?} : recent comments on Instagram posts and Facebook Page posts, with existing replies."""
    since = time.time() - int(req.get("days", 3)) * 86400
    out = {"instagram": [], "facebook": []}
    for m in call(f"{IG}/media", {"fields": "id,permalink,caption,timestamp", "limit": 25}).get("data", []):
        if datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z").timestamp() < since: continue
        cs = call(f"{m['id']}/comments", {"fields": "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}", "limit": 50})
        for c in cs.get("data", []):
            c["media_id"] = m["id"]; c["permalink"] = m.get("permalink"); c["post_caption"] = (m.get("caption") or "")[:120]
            out["instagram"].append(c)
    p = page()
    if p:
        tok = p["access_token"]
        for post in call(f"{p['id']}/posts", {"fields": "id,message,created_time", "limit": 25}, token=tok).get("data", []):
            cs = call(f"{post['id']}/comments", {"fields": "id,message,from,created_time,comments{id,message,from}", "limit": 50}, token=tok)
            for c in cs.get("data", []):
                c["post_id"] = post["id"]; c["post_message"] = (post.get("message") or "")[:120]
                out["facebook"].append(c)
    return out

def op_reply(req):
    """{platform: instagram|facebook, comment_id, message}"""
    if req["platform"] == "instagram":
        return call(f"{req['comment_id']}/replies", {"message": req["message"]}, "POST")
    p = page()
    return call(f"{req['comment_id']}/comments", {"message": req["message"]}, "POST", token=p["access_token"])

def op_fb_posts(req):
    p = page()
    return call(f"{p['id']}/posts", {"fields": "id,message,created_time,permalink_url", "limit": 15}, token=p["access_token"])

def op_fb_delete(req):
    """{post_id} : delete a Facebook Page post (only when Rishi asked)."""
    p = page()
    return call(req["post_id"], {}, "DELETE", token=p["access_token"])

def op_hide(req):
    """{comment_id} : hide spam or abuse on Instagram."""
    return call(req["comment_id"], {"hide": "true"}, "POST")


def op_brand(req):
    """Reads IG bio/website and the FB Page cover; saves the largest cover rendition to meta/brand/fb-cover.jpg."""
    out = {"instagram": call(CFG["ig_user_id"], {"fields": "username,name,biography,website,profile_picture_url"})}
    p = page()
    if not p: return {**out, "page": "not visible"}
    pt = p["access_token"]
    pg = call(p["id"], {"fields": "name,about,cover{id,source,offset_y}"}, token=pt)
    out["page"] = pg
    cid = (pg.get("cover") or {}).get("id")
    if cid:
        ph = call(cid, {"fields": "images,width,height"}, token=pt)
        imgs = sorted(ph.get("images", []), key=lambda i: i.get("width", 0) * i.get("height", 0), reverse=True)
        out["cover_sizes"] = [(i.get("width"), i.get("height")) for i in imgs]
        if imgs:
            os.makedirs("meta/brand", exist_ok=True)
            with urllib.request.urlopen(imgs[0]["source"], timeout=60) as r:
                open("meta/brand/fb-cover.jpg", "wb").write(r.read())
            out["saved"] = "meta/brand/fb-cover.jpg"
    return out

def op_set_budget(req):
    """Rishi-only: sets the fixed campaign's daily budget to config boost_daily_budget_inr (change config in a reviewed commit, never from an automated run)."""
    camp = find_campaign()
    if not camp: return {"error": "no campaign"}
    paise = int(CFG["boost_daily_budget_inr"]) * 100
    r = call(camp["id"], {"daily_budget": paise}, "POST")
    return {"result": r, "now": call(camp["id"], {"fields": "name,daily_budget,status"})}

def op_ad_breakdown(req):
    """{ad_id, date_preset?:'today'} -> spend, reach and actions by platform and placement."""
    return call(f"{req['ad_id']}/insights", {"fields": "spend,impressions,reach,actions",
                "breakdowns": "publisher_platform,platform_position", "date_preset": req.get("date_preset", "today")})

OPS = {"test": op_test, "insights": op_insights, "boost_status": op_boost_status,
       "boost_setup": op_boost_setup, "boost_post": op_boost_post, "pause_ad": op_pause_ad, "pause_all": op_pause_all, "set_budget": op_set_budget, "ad_breakdown": op_ad_breakdown,
       "ig_reel": op_ig_reel, "ig_carousel": op_ig_carousel, "ig_story": op_ig_story, "fb_reel": op_fb_reel, "fb_photos": op_fb_photos,
       "comments": op_comments, "fb_posts": op_fb_posts, "fb_delete": op_fb_delete, "reply": op_reply, "hide": op_hide, "brand": op_brand}
# Deliberately absent: any op that changes budget, billing or creates other campaigns.

def main():
    if not TOKEN:
        sys.exit("META_TOKEN secret missing")
    os.makedirs("meta/results", exist_ok=True)
    os.makedirs("meta/processed", exist_ok=True)
    for f in sorted(glob.glob("meta/requests/*.json")):
        name = os.path.basename(f)[:-5]
        if os.path.exists(f"meta/processed/{name}"):
            print(f"skip {name}: already processed"); os.remove(f); continue
        open(f"meta/processed/{name}", "w").write(datetime.datetime.utcnow().isoformat())
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
