#!/usr/bin/env python3
"""Daily learning run: IG media + account, Facebook per post, cross-platform view.
Usage: python3 scripts/learn_daily.py <insights.json> <boost_status.json> <platforms.json> <date>
Writes learnings/data/<date>-media.csv, -account.csv, -facebook.csv, -cross.csv."""
import json, sys, csv, datetime, statistics, re, glob, os

ins_f, boost_f, plat_f, day = sys.argv[1:5]
I = json.load(open(ins_f)); ins = I["result"]; boost = json.load(open(boost_f))["result"]; plat = json.load(open(plat_f))["result"]
now = datetime.datetime.strptime(I["ran_at"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)

# Join table from log.md, keyed by IG media id (surviving copy; trial twins replaced deleted mains on 18 Nov).
M = {
 "18341456980274380": dict(key="2026-11-16-delhi", title="Why Delhi has no skyscrapers", fmt="reel", hook="1 contradiction", story="city mystery", look="A Newsroom Red", voice="Jessa", shot="photoreal AI event", geo="India", length_s=57.05, slot="midday", trial="no", followcard="no", send="city friends in NCR"),
 "18131037979847506": dict(key="2026-11-16-noida", title="Noida twin towers blown up", fmt="reel", hook="1 contradiction + stakes", story="real case timeline", look="A Newsroom Red", voice="Tara", shot="photoreal AI event", geo="India", length_s=54.6, slot="evening", trial="no", followcard="no", send="friend buying a flat in NCR"),
 "18086326760340689": dict(key="2026-11-17-midday", title="Japan houses lose value (trial)", fmt="reel", hook="1 contradiction", story="counterintuitive economics", look="F Tokyo Neutral", voice="Jessa", shot="split frame AI", geo="global", length_s=53.1, slot="midday", trial="yes", followcard="no", send="friend who says property always goes up"),
 "18455422555132731": dict(key="2026-11-17-evening", title="Burj Khalifa on sand", fmt="reel", hook="1 contradiction", story="how it works (engineering)", look="E Blueprint", voice="George", shot="line art cutaway", geo="global", length_s=47.6, slot="evening", trial="no", followcard="no", send="friend who has been to Dubai"),
 "18508881529100400": dict(key="2026-11-18-midday", title="Steel rods on Indian roofs (trial)", fmt="reel", hook="24 why does X look like this", story="weird / hidden in plain sight", look="C Midnight Gold", voice="Tara", shot="real photo, bright rooftops", geo="India", length_s=52.0, slot="midday", trial="yes", followcard="no", send="family WhatsApp group"),
 "17995953015110577": dict(key="2026-11-18-evening", title="Jakarta sinking, new capital", fmt="reel", hook="10 visual shock", story="visual shock with a decision", look="T TrueYards Brand", voice="Jessa", shot="impossible-real AI", geo="global", length_s=55.0, slot="evening", trial="no", followcard="yes", send="friend who follows climate news"),
 "18111012790950337": dict(key="2026-11-15-evening", title="Untitled reel 15 Nov (unlogged)", fmt="reel", hook="unlogged", story="unlogged", look="", voice="", shot="", geo="", length_s=None, slot="evening", trial="no", followcard="no", send=""),
 "17897931087682587": dict(key="2026-11-14-reel", title="Rs 50 lakh loan costs Rs 1.04 crore", fmt="reel", hook="2 number slam", story="money maths", look="bone/red 3D", voice="", shot="3D render", geo="India", length_s=24.0, slot="evening", trial="no", followcard="no", send=""),
 "18178380412407784": dict(key="2026-11-19-midday", title="Why Jaipur is pink (trial)", fmt="reel", hook="14 story cold open", story="history with a property twist", look="B Emerald Doc", voice="George", shot="impossible-real AI", geo="India", length_s=54.1, slot="midday", trial="yes", followcard="yes", send="anyone who has been to Jaipur; family group"),
 "18228143677338500": dict(key="2026-11-19-evening", title="Mumbai Rs 1,300 rent flat (trial)", fmt="reel", hook="2 number slam", story="money maths (real case with a twist)", look="T TrueYards Brand", voice="Tara", shot="render (photoreal AI)", geo="India", length_s=48.5, slot="evening", trial="yes", followcard="yes", send="friend who rents in Mumbai"),
 "17918934828546266": dict(key="2026-11-19-carousel", title="Property prices never fall? carousel", fmt="carousel", hook="5 myth bust + 2 number slam", story="myth bust with data cards", look="T TrueYards Brand light", geo="global + India"),
 "17915522373487439": dict(key="2026-11-20-midday", title="SC shields stalled-project buyers (trial)", fmt="reel", hook="1 contradiction on an object (news)", story="news explained", look="A Newsroom Red", voice="Jessa", shot="photoreal AI stalled tower", geo="India", length_s=55.0, slot="midday", trial="yes", followcard="yes", send="anyone paying EMI on an under-construction flat"),
 "18615292321064108": dict(key="2026-11-20-evening", title="Kerala locked empty houses (trial)", fmt="reel", hook="1 contradiction", story="mystery (India)", look="T TrueYards Brand", voice="George", shot="photoreal AI bright house", geo="India", length_s=52.1, slot="evening", trial="yes", followcard="yes", send="every Malayali, Gulf families"),
 "17919760626494721": dict(key="2026-11-20-carousel", title="Start here carousel (to pin)", fmt="carousel", hook="24 why does X look like this (list)", story="index / promise", look="T TrueYards Brand light", geo="India"),
 "17940674607125722": dict(key="2026-11-21-midday", title="Hong Kong homes smaller than parking (trial)", fmt="reel", hook="1 contradiction (full-frame motion open, X14)", story="global comparison", look="F Tokyo Neutral", voice="Jessa", shot="full-frame motion, bright AI", geo="global", length_s=51.4, slot="midday", trial="yes", followcard="yes", send="friend who says their flat is tiny"),
 "18140554237642623": dict(key="2026-11-21-evening", title="Aangan courtyard hole in the middle (trial)", fmt="reel", hook="1 contradiction (full-frame motion open, D41)", story="engineering marvel (low-tech climate)", look="T TrueYards Brand", voice="Tara", shot="full-frame motion push-in, bright AI", geo="India", length_s=46.6, slot="evening", trial="yes", followcard="yes", send="family WhatsApp group"),
 "17954408460050031": dict(key="2026-11-22-midday", title="Shani Shingnapur no front doors (trial)", fmt="reel", hook="24 why does X look like this", story="real case / weird hidden in plain sight", look="B Emerald Doc", voice="George", shot="full-frame motion push-in, bright AI", geo="India", length_s=56.0, slot="midday", trial="yes", followcard="voiced outro (X15)", send="family WhatsApp group"),
 "18131749264842833": dict(key="2026-11-22-carousel-reel", title="Carpet vs super built-up area (trial)", fmt="reel", hook="1 contradiction on a bright object", story="myth bust / money maths", look="F Tokyo Neutral", voice="Jessa", shot="full-frame motion push-in, bright AI", geo="India", length_s=59.0, slot="afternoon", trial="yes", followcard="silent card (X15)", send="friend buying a flat"),
 "17920086021259928": dict(key="2026-11-22-evening", title="Bengaluru bus station was a lake (trial)", fmt="reel", hook="1 contradiction on a famous place", story="history (land before the city)", look="T TrueYards Brand", voice="Tara", shot="full-frame motion push-in, impossible-real AI", geo="India", length_s=59.6, slot="evening", trial="yes", followcard="voiced outro (X15)", send="every Bengalurean"),
 "18084884045431961": dict(key="2026-11-23-carousel", title="Rs 1 crore flat costs Rs 1.14 crore carousel", fmt="carousel", hook="2 number slam + checklist", story="money maths / hidden costs", look="T TrueYards Brand light", geo="India"),
 "17916533091559974": dict(key="2026-11-23-evening", title="Steinway Tower 435 m tall 18 m wide", fmt="reel", hook="23 scale awe", story="engineering marvel (global, Indian framing)", look="T TrueYards Brand", voice="George", shot="full-frame tilt up, impossible-real AI", geo="global", length_s=51.9, slot="evening", trial="no", followcard="silent card (X15)", send="friend into architecture; anyone who has been to New York"),
 "18038784548709035": dict(key="2026-11-24-midday", title="Chandigarh no Sector 13", fmt="reel", hook="1 contradiction on a famous place", story="mystery (India)", look="B Emerald Doc", voice="George", shot="impossible-real AI, planned grid", geo="India", length_s=50.4, slot="midday", trial="no", followcard="voiced outro (X15)", send="anyone from Chandigarh, Mohali or Panchkula"),
 "17970572490219322": dict(key="2026-11-24-carousel", title="Mumbai flats with no OC, families left", fmt="reel", hook="1 contradiction", story="real case told as a myth bust", look="A Newsroom Red", voice="Tara", shot="impossible-real AI tower", geo="India", length_s=44.8, slot="afternoon", trial="no", followcard="silent card (X15)", send="anyone about to take possession of a flat"),
 "18114493301598863": dict(key="2026-11-24-evening", title="Every Indian balcony has an iron grill", fmt="reel", hook="24 why does X look like this", story="weird / hidden in plain sight", look="T TrueYards Brand", voice="Jessa", shot="impossible-real AI birdcage block", geo="India", length_s=51.2, slot="evening", trial="no", followcard="voiced outro (X15)", send="family WhatsApp group"),
 "18406492459202075": dict(key="2026-11-25-midday", title="Flat or plot? What you really own", fmt="reel", hook="16 versus into 1 contradiction", story="myth bust (family debate), X19 shares", look="F Tokyo Neutral", voice="Tara", shot="impossible-real AI tower lifted off plot", geo="India", length_s=43.6, slot="midday", trial="no", followcard="silent card (X15)", send="family member who wants a plot"),
 "18488610967114054": dict(key="2026-11-25-carousel", title="Getting your keys? 7 checks carousel", fmt="carousel", hook="4 stakes + 26 countdown", story="checklist / buyer protection", look="T TrueYards Brand light", geo="India"),
 "18034638014683408": dict(key="2026-11-25-evening", title="Ahmedabad pols escape routes", fmt="reel", hook="1 contradiction on a famous place", story="history (famous old city), X19 control", look="T TrueYards Brand", voice="Jessa", shot="photoreal AI of a real place, push down lane", geo="India", length_s=51.6, slot="evening", trial="no", followcard="voiced outro (X15)", send="every Amdavadi"),
 "18136597870808638": dict(key="2026-11-26-midday", title="Gold or property family fight", fmt="reel", hook="1 contradiction (family argument)", story="money maths, X19 shares", look="C Midnight Gold", voice="Tara", shot="photoreal AI gold and balconies", geo="India", length_s=50.8, slot="midday", trial="no", followcard="silent card (X15)", send="the uncle who says property never falls"),
 "18125641003737710": dict(key="2026-11-26-evening", title="Why India looks like this #1 Dharavi", fmt="reel", hook="24 why does X look like this", story="visual shock into redevelopment maths, X19 control", look="B Emerald Doc", voice="Jessa", shot="bright full-frame aerial, real place", geo="India", length_s=50.9, slot="evening", trial="no", followcard="voiced outro (X15)", send="every Mumbaikar"),
 "18099738566652487": dict(key="", title="Forteasia project reel (exclude)", fmt="reel", exclude=True),
 "18120271354823510": dict(key="2026-11-18-carousel", title="Delhi Mumbai Expressway carousel", fmt="carousel", hook="1 contradiction + 2 number slam", story="timeline / map", look="Bone Road", geo="India"),
 "18196361215397123": dict(key="2026-11-17-carousel", title="Stamp duty by buyer carousel", fmt="carousel", hook="2 number slam + 16 versus", story="money rules", look="C Midnight Gold", geo="India"),
 "17969838036213337": dict(key="2026-11-16-pizza", title="Super built-up area, Aarav pizza", fmt="carousel", hook="story explainer", story="rules", look="H Explained to a beginner", geo="India"),
 "17919778947535616": dict(key="2026-11-16-boldtype", title="LEGAL? RERA, CC, OC", fmt="carousel", hook="18 insider words", story="rules", look="G Bold Type", geo="India"),
 "17880307479565603": dict(key="2026-11-15-carousel", title="Warehousing record (Vestian)", fmt="carousel", hook="2 number slam", story="news", look="tc", geo="India"),
 "18100287476670109": dict(key="2026-11-14-papers", title="Six papers before a plot", fmt="carousel", hook="4 stakes", story="rules", look="tb", geo="India"),
 "18106043462027996": dict(key="2026-11-14-carpet", title="1,200 sq ft flat really 800", fmt="carousel", hook="1 contradiction", story="rules", look="", geo="India"),
}
boosted = {}
for a in boost.get("ads", {}).get("data", []):
    mid = (a.get("creative") or {}).get("source_instagram_media_id")
    if mid: boosted.setdefault(mid, []).append(a["name"])

acct = ins["instagram_account"]; followers_now = acct["profile"]["followers_count"]
rows = []
for m in ins["instagram_media"]:
    i = m["insights"]; meta = M.get(m["id"], dict(key="", title=(m.get("caption") or "")[:50], fmt=m["media_product_type"].lower()))
    ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z"); age = (now - ts).total_seconds() / 3600
    reach = i.get("reach") or 0
    per = lambda v: round(100 * v / reach, 2) if reach and v is not None else ""
    L = meta.get("length_s"); aw = i.get("ig_reels_avg_watch_time")
    fol = i.get("follows"); pv = i.get("profile_visits")
    rows.append(dict(media_id=m["id"], key=meta.get("key", ""), date_utc=m["timestamp"][:16], age_h=round(age, 1), final="yes" if age >= 72 else "no",
        boosted="yes" if m["id"] in boosted else "no", exclude="yes" if meta.get("exclude") else "no", trial=meta.get("trial", ""),
        title=meta["title"], format=meta.get("fmt"), hook=meta.get("hook", ""), story_type=meta.get("story", ""), look=meta.get("look", ""),
        voice=meta.get("voice", ""), opening_shot=meta.get("shot", ""), geo=meta.get("geo", ""), language="English", length_s=L or "",
        slot=meta.get("slot", ""), follow_card=meta.get("followcard", ""), send_test=meta.get("send", ""),
        reach=reach, views=i.get("views"), likes=i.get("likes"), comments=i.get("comments"), shares=i.get("shares"), saves=i.get("saved"),
        follows=fol if fol is not None else "", profile_visits=pv if pv is not None else "",
        follows_per_1k_reach=round(1000 * fol / reach, 2) if fol is not None and reach else "",
        profile_visits_per_reach_pct=per(pv) if pv is not None else "",
        avg_watch_s=round(aw / 1000, 1) if aw else "", skip_rate=i.get("reels_skip_rate") if i.get("reels_skip_rate") is not None else "",
        sends_per_reach_pct=per(i.get("shares") or 0), saves_per_reach_pct=per(i.get("saved") or 0), likes_per_reach_pct=per(i.get("likes") or 0),
        hold_ratio_pct=round(100 * aw / 1000 / L, 1) if L and aw else "", views_per_reach=round(i["views"] / reach, 2) if reach else ""))

org = [x for x in rows if x["exclude"] == "no"]
def pct(v, pool):
    pool = [p for p in pool if p not in ("", None)]
    return "" if v in ("", None) or not pool else round(100 * sum(1 for p in pool if p <= v) / len(pool))
for x in rows:
    pool = [y for y in org if y["format"] == x["format"]]
    for k in ("reach", "sends_per_reach_pct", "saves_per_reach_pct", "hold_ratio_pct", "views_per_reach", "likes_per_reach_pct"):
        x[f"pctl_{k}"] = pct(x[k], [y[k] for y in pool])
    sk = [y["skip_rate"] for y in pool if y["skip_rate"] != ""]
    x["pctl_low_skip"] = round(100 * sum(1 for s in sk if s >= x["skip_rate"]) / len(sk)) if x["skip_rate"] != "" and sk else ""
    others = [y["reach"] for y in pool if y["media_id"] != x["media_id"]]; med = statistics.median(others) if others else 0
    flag = []
    if x["exclude"] == "yes": flag.append("excluded (Forteasia)")
    else:
        if x["boosted"] == "yes": flag.append("boosted from 18 Nov 05:14 UTC (IG post insights are organic only; ad numbers in BOOST_LOG)")
        if x["final"] == "no":
            if med and x["reach"] >= 3 * med and (x["sends_per_reach_pct"] or 0) >= 1: flag.append("BREAKOUT")
            elif med and x["reach"] >= 3 * med: flag.append("reach breakout, sends under 1%")
            if x["format"] == "reel" and x["skip_rate"] != "" and x["skip_rate"] >= 60: flag.append("dud signal: skip 60%+")
        if x["trial"] == "yes" and x["age_h"] >= 24 and x["skip_rate"] != "" and x["skip_rate"] < 35 and (x["hold_ratio_pct"] or 0) >= 45 and 1000 * (x["shares"] or 0) / max(1, x["reach"]) >= 2:
            flag.append("STRONG TRIAL (D18)")
    x["flag"] = "; ".join(flag); x["format_median_reach_others"] = med

with open(f"learnings/data/{day}-media.csv", "w", newline="") as f:
    w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)

reach = {v["end_time"][:10]: v["value"] for v in acct["daily"]["data"][0]["values"]}
newf = {v["end_time"][:10]: v["value"] for v in acct["daily"]["data"][1]["values"]}
with open(f"learnings/data/{day}-account.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["day_end_utc", "reach", "new_followers"])
    for d in sorted(reach): w.writerow([d, reach[d], newf.get(d, "")])
    w.writerow([f"snapshot {now.isoformat()}", "", f"followers_count={followers_now}"])

# Facebook per post
fb = ins["facebook"]; fbrows = []
for p in fb.get("posts", []):
    i = p.get("insights", {}); desc = (p.get("description") or "").split("\n")[0][:60]
    if "Rohtak" in (p.get("description") or "") or "FIT" in desc: continue
    soc = i.get("post_video_social_actions") or {}
    reac = i.get("reactions") if "reactions" in i else sum((i.get("post_video_likes_by_reaction_type") or {}).values())
    fbrows.append(dict(kind=p["kind"], id=p.get("video_id") or p["post_id"], created=p["created_time"][:16], title=desc,
        plays=i.get("fb_reels_total_plays", ""), avg_watch_s=round(i["post_video_avg_time_watched"] / 1000, 1) if i.get("post_video_avg_time_watched") else "",
        reactions=reac or 0, comments=i.get("comments", soc.get("COMMENT", 0)) or 0, shares=i.get("shares", soc.get("SHARE", 0)) or 0,
        media_views=i.get("post_media_view", ""), followers_gained=i.get("post_video_followers", "")))
with open(f"learnings/data/{day}-facebook.csv", "w", newline="") as f:
    w = csv.DictWriter(f, list(fbrows[0].keys())); w.writeheader(); w.writerows(fbrows)

# cross-platform
fbkey = {}
for r in fbrows:
    for x in rows:
        if x["key"] and abs((datetime.datetime.fromisoformat(r["created"]) - datetime.datetime.fromisoformat(x["date_utc"])).total_seconds()) < 900 and \
           ((r["kind"] == "reel") == (x["format"] == "reel")):
            fbkey[x["key"]] = r
cross = {}
for x in rows:
    if not x["key"]: continue
    c = cross.setdefault(x["key"], dict(key=x["key"], ig_media=x["media_id"], title=x["title"], format=x["format"]))
    c["ig_views"] = x["views"]; c["ig_eng"] = (x["likes"] or 0) + (x["comments"] or 0) + (x["shares"] or 0) + (x["saves"] or 0)
    r = fbkey.get(x["key"])
    if r: c["fb_views"] = r["plays"] if r["plays"] != "" else r["media_views"]; c["fb_eng"] = r["reactions"] + r["comments"] + r["shares"]
for r in plat["rows"]:
    c = cross.setdefault(r["post"], dict(key=r["post"], ig_media="", title="", format=""))
    p = r["platform"]; c[f"{p}_views"] = r["views"] or 0
    c[f"{p}_eng"] = sum((r.get(k) or 0) for k in ("likes", "comments", "shares", "saves"))
plats = ["ig", "fb", "yt", "threads", "x"]
for p in plats:
    have = [c for c in cross.values() if c.get(f"{p}_views") not in (None, "")]
    for c in have:
        v = c[f"{p}_views"] or 0; c[f"{p}_epv"] = round(c[f"{p}_eng"] / v, 4) if v else 0
    for c in have:
        c[f"{p}_epv_pct"] = pct(c[f"{p}_epv"], [d[f"{p}_epv"] for d in have]); c[f"{p}_views_pct"] = pct(c[f"{p}_views"], [d[f"{p}_views"] for d in have])
cols = ["key", "ig_media", "title", "format"] + [f"{p}_{k}" for p in plats for k in ("views", "eng", "epv", "epv_pct", "views_pct")]
with open(f"learnings/data/{day}-cross.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
    for k in sorted(cross): w.writerow(cross[k])

for x in rows:
    if x["exclude"] == "no":
        print(x["title"][:34].ljust(35), x["age_h"], x["reach"], "skip", x["skip_rate"], "hold", x["hold_ratio_pct"], "send", x["sends_per_reach_pct"], "save", x["saves_per_reach_pct"], "like", x["likes_per_reach_pct"], "v/r", x["views_per_reach"], "pv", x["profile_visits"], x["flag"])
print("--- cross")
for k in sorted(cross):
    c = cross[k]; print(k, *[f"{p}:{c.get(p+'_views','')}/{c.get(p+'_eng','')} p{c.get(p+'_views_pct','')}" for p in plats])
