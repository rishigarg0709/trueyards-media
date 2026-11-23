#!/usr/bin/env python3
"""Daily learning metrics: meta/results insights JSON -> learnings/data/<date>-media.csv and -account.csv.
Usage: python3 scripts/learn_metrics.py <insights.json> <boost_status.json> <date>"""
import json, sys, csv, datetime, statistics

ins_f, boost_f, day = sys.argv[1:4]
ins = json.load(open(ins_f))["result"]; boost = json.load(open(boost_f))["result"]
now = datetime.datetime.strptime(json.load(open(ins_f))["ran_at"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)

# Join table from log.md (manual, keyed by media id). length_s from ffprobe of the draft file.
META = {
 "18341456980274380": dict(title="Why Delhi has no skyscrapers", fmt="reel", hook="1 contradiction (forbidden)", story="mystery", geo="India", lang="English", length_s=57.05, accent="red/white", voice="Jessa", music="96 BPM beat dl-beat-1", slot="midday", send="city friends in NCR"),
 "18131037979847506": dict(title="Noida twin towers blown up", fmt="reel", hook="1 contradiction + stakes", story="story timeline", geo="India", lang="English", length_s=54.6, accent="A Newsroom Red", voice="Tara", music="tense cinematic trap 96 BPM", slot="evening", send="friend buying a flat in NCR"),
 "18111012790950337": dict(title="Untitled reel 15 Nov (DfxHQD6vKff, not in log.md)", fmt="reel", hook="unlogged", story="unlogged", geo="", lang="", length_s=None, accent="", voice="", music="", slot="evening", send=""),
 "17897931087682587": dict(title="Rs 50 lakh loan costs Rs 1.04 crore", fmt="reel", hook="2 number slam (inferred)", story="money", geo="India", lang="English", length_s=24.0, accent="bone/red", voice="", music="Stylish Trailer Percussion", slot="evening", send=""),
 "18099738566652487": dict(title="Forteasia project reel (exclude)", fmt="reel", hook="n/a", story="Forteasia", geo="India", lang="", length_s=None, accent="", voice="", music="", slot="", send="", exclude=True),
 "17969838036213337": dict(title="Super built-up area, Aarav pizza", fmt="carousel", hook="story explainer", story="rules", geo="India", lang="English", length_s=None, accent="look H", voice="", music="", slot="evening", send=""),
 "17919778947535616": dict(title="LEGAL? RERA, CC, OC", fmt="carousel", hook="18 insider words", story="rules", geo="India", lang="English", length_s=None, accent="look G Bold Type", voice="", music="", slot="midday", send=""),
 "17880307479565603": dict(title="India warehousing record (Vestian)", fmt="carousel", hook="2 number slam (inferred)", story="news", geo="India", lang="English", length_s=None, accent="look tc", voice="", music="", slot="midday", send=""),
 "18100287476670109": dict(title="Six papers before you pay for a plot", fmt="carousel", hook="4 stakes (inferred)", story="rules", geo="India", lang="English", length_s=None, accent="look tb", voice="", music="", slot="midday", send=""),
 "18106043462027996": dict(title="1,200 sq ft flat that is really 800", fmt="carousel", hook="1 contradiction (inferred)", story="rules", geo="India", lang="English", length_s=None, accent="", voice="", music="", slot="morning", send=""),
}
boosted = set()
for a in boost.get("ads", {}).get("data", []):
    c = a.get("creative", {}) or {}
    if c.get("source_instagram_media_id"): boosted.add(c["source_instagram_media_id"])

rows = []
for m in ins["instagram_media"]:
    i = m["insights"]; meta = META.get(m["id"], dict(title=m.get("caption", "")[:50], fmt=m["media_product_type"].lower()))
    ts = datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
    age_h = (now - ts).total_seconds() / 3600
    reach = i.get("reach") or 0
    r = lambda k: round(100 * (i.get(k) or 0) / reach, 2) if reach else None
    L = meta.get("length_s")
    hold = round(100 * i["ig_reels_avg_watch_time"] / 1000 / L, 1) if L and i.get("ig_reels_avg_watch_time") else None
    rows.append(dict(media_id=m["id"], date_utc=m["timestamp"][:16], age_h=round(age_h, 1), final="yes" if age_h >= 72 else "no",
        boosted="yes" if m["id"] in boosted else "no", exclude="yes" if meta.get("exclude") else "no",
        title=meta.get("title"), format=meta.get("fmt"), hook=meta.get("hook", ""), story_type=meta.get("story", ""), geo=meta.get("geo", ""),
        language=meta.get("lang", ""), length_s=L or "", accent_look=meta.get("accent", ""), voice=meta.get("voice", ""), music=meta.get("music", ""),
        slot=meta.get("slot", ""), send_test=meta.get("send", ""),
        reach=reach, views=i.get("views"), likes=i.get("likes"), comments=i.get("comments"), shares=i.get("shares"), saves=i.get("saved"),
        avg_watch_s=round(i["ig_reels_avg_watch_time"] / 1000, 1) if i.get("ig_reels_avg_watch_time") else "",
        skip_rate=i.get("reels_skip_rate", ""), sends_per_reach_pct=r("shares"), saves_per_reach_pct=r("saved"),
        likes_per_reach_pct=r("likes"), hold_ratio_pct=hold if hold is not None else "",
        views_per_reach=round(i["views"] / reach, 2) if reach else None, profile_visits=i.get("profile_visits", "")))

# percentiles vs trailing 30 days, organic TrueYards only, within format
org = [x for x in rows if x["exclude"] == "no" and x["boosted"] == "no"]
def pct(val, pool):
    pool = [p for p in pool if p not in ("", None)]
    if val in ("", None) or not pool: return ""
    return round(100 * sum(1 for p in pool if p <= val) / len(pool))
for x in rows:
    pool = [y for y in org if y["format"] == x["format"]]
    for k in ("reach", "sends_per_reach_pct", "saves_per_reach_pct", "hold_ratio_pct", "views_per_reach"):
        x[f"pctl_{k}"] = pct(x[k], [y[k] for y in pool])
    x["pctl_skip_low_is_good"] = (100 - pct(x["skip_rate"], [y["skip_rate"] for y in pool]) + round(100 / max(1, len([y for y in pool if y["skip_rate"] != ""])))) if x["skip_rate"] != "" else ""
    # flags (playbook section 6)
    reel_reach = [y["reach"] for y in pool if y["media_id"] != x["media_id"]]
    med = statistics.median(reel_reach) if reel_reach else 0
    flag = []
    if x["exclude"] == "yes": flag.append("excluded (Forteasia)")
    elif x["final"] == "no":
        if med and x["reach"] >= 3 * med and (x["sends_per_reach_pct"] or 0) >= 1: flag.append("BREAKOUT")
        elif med and x["reach"] >= 3 * med: flag.append("reach breakout, sends below 1% (not a full breakout)")
        if x["skip_rate"] != "" and x["skip_rate"] >= 80: flag.append("dud: skip")
    x["flag"] = "; ".join(flag)
    x["format_median_reach_others"] = med

keys = list(rows[0].keys())
with open(f"learnings/data/{day}-media.csv", "w", newline="") as f:
    w = csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)

acct = ins["instagram_account"]
reach = {v["end_time"][:10]: v["value"] for v in acct["daily"]["data"][0]["values"]}
fol = {v["end_time"][:10]: v["value"] for v in acct["daily"]["data"][1]["values"]}
with open(f"learnings/data/{day}-account.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["day_end", "reach", "new_followers"])
    for d in sorted(reach): w.writerow([d, reach[d], fol.get(d, "")])
    w.writerow([f"snapshot {now.isoformat()}", "", f"followers_count={acct['profile']['followers_count']}"])
for x in rows:
    print(x["title"][:34].ljust(35), x["age_h"], x["reach"], x["skip_rate"], x["hold_ratio_pct"], x["sends_per_reach_pct"], x["saves_per_reach_pct"], x["likes_per_reach_pct"], x["views_per_reach"], x["flag"])
