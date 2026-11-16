#!/usr/bin/env python3
"""Cross-posting to YouTube Shorts, Threads and X. Reads social/requests/*.json, writes social/results/<name>.json.
Keys come only from GitHub secrets and are never written or printed."""
import base64, datetime, glob, hashlib, hmac, json, os, secrets, sys, time, urllib.parse, urllib.request, urllib.error

E = os.environ.get
UA = {"User-Agent": "TrueYardsBot/1.0"}

def http(url, data=None, headers=None, method=None, raw=False, timeout=300):
    h = dict(UA); h.update(headers or {})
    if isinstance(data, (dict, list)):
        data = json.dumps(data).encode(); h.setdefault("Content-Type", "application/json")
    elif isinstance(data, str):
        data = data.encode()
    r = urllib.request.Request(url, data=data, headers=h, method=method or ("POST" if data is not None else "GET"))
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            b = resp.read(); return (resp.headers, b) if raw else (json.loads(b) if b else {})
    except urllib.error.HTTPError as e:
        body = e.read()[:600].decode(errors="replace")
        return {"error": f"HTTP {e.code}", "body": body}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        return r.read()

# ---------- YouTube Shorts ----------
def yt_token():
    j = http("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
        "client_id": E("YT_CLIENT_ID"), "client_secret": E("YT_CLIENT_SECRET"),
        "refresh_token": E("YT_REFRESH_TOKEN"), "grant_type": "refresh_token"}),
        {"Content-Type": "application/x-www-form-urlencoded"})
    return j.get("access_token"), j

def op_yt_short(req):
    """{video_url, title (<=100), description, tags?, privacy? public|unlisted|private}"""
    tok, j = yt_token()
    if not tok: return {"auth_error": j}
    vid = fetch(req["video_url"])
    title = req["title"][:95]
    if "#shorts" not in title.lower() and len(title) < 88: title += " #Shorts"
    meta = {"snippet": {"title": title, "description": req.get("description", ""), "tags": req.get("tags", []), "categoryId": "27"},
            "status": {"privacyStatus": req.get("privacy", "public"), "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}}
    hdr = {"Authorization": f"Bearer {tok}", "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(len(vid))}
    res = http("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", meta, hdr, raw=True)
    if isinstance(res, dict): return {"init_error": res}
    loc = res[0].get("Location")
    up = http(loc, vid, {"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"}, method="PUT", timeout=600)
    if "id" in up:
        return {"video_id": up["id"], "url": f"https://youtube.com/shorts/{up['id']}", "privacy": up.get("status", {}).get("privacyStatus")}
    return {"upload_error": up}

def op_yt_check(req):
    tok, j = yt_token()
    if not tok: return {"auth_error": j}
    return http("https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true", headers={"Authorization": f"Bearer {tok}"})

def op_yt_stats(req):
    """{video_ids:[...]}"""
    tok, j = yt_token()
    if not tok: return {"auth_error": j}
    ids = ",".join(req["video_ids"])
    return http(f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={ids}", headers={"Authorization": f"Bearer {tok}"})

# ---------- Threads ----------
TH = "https://graph.threads.net/v1.0"
def th(path, params, method="POST"):
    p = dict(params); p["access_token"] = E("THREADS_TOKEN")
    url = f"{TH}/{path}"
    if method == "GET": return http(url + "?" + urllib.parse.urlencode(p))
    return http(url, urllib.parse.urlencode(p), {"Content-Type": "application/x-www-form-urlencoded"})

def th_wait(cid):
    for _ in range(40):
        s = th(cid, {"fields": "status,error_message"}, "GET")
        if s.get("status") in ("FINISHED", "ERROR", "EXPIRED", "PUBLISHED"): return s
        time.sleep(10)
    return s

def op_threads_post(req):
    """{text, video_url? | image_urls?[...]} : one post (video, single image, carousel or text)."""
    me = th("me", {"fields": "id,username"}, "GET")
    if "id" not in me: return {"auth_error": me}
    uid = me["id"]; text = req.get("text", "")[:500]
    if req.get("video_url"):
        c = th(f"{uid}/threads", {"media_type": "VIDEO", "video_url": req["video_url"], "text": text})
    elif req.get("image_urls") and len(req["image_urls"]) > 1:
        kids = []
        for u in req["image_urls"][:20]:
            k = th(f"{uid}/threads", {"media_type": "IMAGE", "image_url": u, "is_carousel_item": "true"})
            if "id" not in k: return {"child_error": k}
            kids.append(k["id"])
        for k in kids: th_wait(k)
        c = th(f"{uid}/threads", {"media_type": "CAROUSEL", "children": ",".join(kids), "text": text})
    elif req.get("image_urls"):
        c = th(f"{uid}/threads", {"media_type": "IMAGE", "image_url": req["image_urls"][0], "text": text})
    else:
        c = th(f"{uid}/threads", {"media_type": "TEXT", "text": text})
    if "id" not in c: return {"container_error": c}
    st = th_wait(c["id"])
    if st.get("status") not in ("FINISHED", None): return {"status": st}
    return {"published": th(f"{uid}/threads_publish", {"creation_id": c["id"]}), "username": me.get("username")}

def op_threads_refresh(req):
    """Extends the 60-day Threads token; result says when it expires (the value itself is never written)."""
    j = http(f"https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={E('THREADS_TOKEN')}")
    return {"ok": "access_token" in j, "expires_in_days": round(j.get("expires_in", 0) / 86400, 1), "error": j.get("error")}

# ---------- X (OAuth 1.0a user context) ----------
def _pct(s): return urllib.parse.quote(str(s), safe="~")
def x_auth(method, url, params=None):
    o = {"oauth_consumer_key": E("X_API_KEY"), "oauth_nonce": secrets.token_hex(16), "oauth_signature_method": "HMAC-SHA1",
         "oauth_timestamp": str(int(time.time())), "oauth_token": E("X_ACCESS_TOKEN"), "oauth_version": "1.0"}
    allp = {**o, **(params or {})}
    base = "&".join([method, _pct(url), _pct("&".join(f"{_pct(k)}={_pct(v)}" for k, v in sorted(allp.items())))])
    key = f"{_pct(E('X_API_SECRET'))}&{_pct(E('X_ACCESS_SECRET'))}"
    o["oauth_signature"] = base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()
    return "OAuth " + ", ".join(f'{_pct(k)}="{_pct(v)}"' for k, v in sorted(o.items()))

MU = "https://upload.twitter.com/1.1/media/upload.json"
def x_upload(blob, mime, cat):
    p = {"command": "INIT", "total_bytes": str(len(blob)), "media_type": mime, "media_category": cat}
    j = http(MU, urllib.parse.urlencode(p), {"Authorization": x_auth("POST", MU, p), "Content-Type": "application/x-www-form-urlencoded"})
    mid = j.get("media_id_string")
    if not mid: return None, j
    step = 4 * 1024 * 1024
    for i in range(0, len(blob), step):
        bnd = secrets.token_hex(12)
        q = {"command": "APPEND", "media_id": mid, "segment_index": str(i // step)}
        body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"media\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + blob[i:i+step] + f"\r\n--{bnd}--\r\n".encode()
        r = http(MU + "?" + urllib.parse.urlencode(q), body, {"Authorization": x_auth("POST", MU, q), "Content-Type": f"multipart/form-data; boundary={bnd}"})
        if isinstance(r, dict) and r.get("error"): return None, r
    p = {"command": "FINALIZE", "media_id": mid}
    j = http(MU, urllib.parse.urlencode(p), {"Authorization": x_auth("POST", MU, p), "Content-Type": "application/x-www-form-urlencoded"})
    info = j.get("processing_info")
    while info and info.get("state") in ("pending", "in_progress"):
        time.sleep(info.get("check_after_secs", 5))
        q = {"command": "STATUS", "media_id": mid}
        info = http(MU + "?" + urllib.parse.urlencode(q), headers={"Authorization": x_auth("GET", MU, q)}).get("processing_info")
    if info and info.get("state") == "failed": return None, info
    return mid, None

def op_x_post(req):
    """{text (<=280), video_url? | image_urls?[...<=4]}"""
    ids = []
    if req.get("video_url"):
        mid, err = x_upload(fetch(req["video_url"]), "video/mp4", "tweet_video")
        if err: return {"media_error": err}
        ids = [mid]
    for u in (req.get("image_urls") or [])[:4]:
        mid, err = x_upload(fetch(u), "image/jpeg", "tweet_image")
        if err: return {"media_error": err}
        ids.append(mid)
    url = "https://api.twitter.com/2/tweets"
    body = {"text": req["text"][:280]}
    if ids: body["media"] = {"media_ids": ids}
    return http(url, body, {"Authorization": x_auth("POST", url)})

# ---------- competitor scan (Apify Instagram scraper) ----------
def op_ig_scan(req):
    """{usernames:[...], per_user?:12, days?:7} -> top recent public posts with engagement.
    {post_urls:[...], days:3650} -> those specific posts with full captions."""
    urls = req.get("post_urls") or [f"https://www.instagram.com/{u.strip('@')}/" for u in req["usernames"]]
    inp = {"directUrls": urls, "resultsType": "posts", "resultsLimit": int(req.get("per_user", 12)),
           "onlyPostsNewerThan": f"{int(req.get('days', 7))} days", "addParentData": False}
    j = http(f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={E('APIFY_TOKEN')}&timeout=280", inp, timeout=320)
    if isinstance(j, dict): return {"error": j}
    keep = ("ownerUsername", "url", "type", "productType", "timestamp", "caption", "likesCount", "commentsCount", "videoViewCount", "videoPlayCount", "videoDuration", "hashtags", "musicInfo", "ownerFullName")
    rows = [{k: it.get(k) for k in keep} for it in j]
    for r in rows:
        if r.get("caption") and not req.get("post_urls"): r["caption"] = r["caption"][:600]
    return {"count": len(rows), "posts": rows}

# ---------- LinkedIn company page (Community Management API) ----------
LI_ORG = "urn:li:organization:128124088"
def li_h(extra=None):
    h = {"Authorization": f"Bearer {E('LI_TOKEN')}", "LinkedIn-Version": "202510", "X-Restli-Protocol-Version": "2.0.0"}
    h.update(extra or {}); return h

def li_upload(kind, blob):
    """kind: images | videos. Returns asset urn or (None, err)."""
    if kind == "images":
        j = http("https://api.linkedin.com/rest/images?action=initializeUpload", {"initializeUploadRequest": {"owner": LI_ORG}}, li_h())
        v = j.get("value") or {}
        if not v.get("uploadUrl"): return None, j
        http(v["uploadUrl"], blob, {"Authorization": f"Bearer {E('LI_TOKEN')}", "Content-Type": "application/octet-stream"}, method="PUT")
        return v["image"], None
    j = http("https://api.linkedin.com/rest/videos?action=initializeUpload",
             {"initializeUploadRequest": {"owner": LI_ORG, "fileSizeBytes": len(blob), "uploadCaptions": False, "uploadThumbnail": False}}, li_h())
    v = j.get("value") or {}
    if not v.get("uploadInstructions"): return None, j
    etags = []
    for ins in v["uploadInstructions"]:
        r = urllib.request.Request(ins["uploadUrl"], data=blob[ins["firstByte"]:ins["lastByte"] + 1], method="PUT",
                                   headers={"Content-Type": "application/octet-stream"})
        with urllib.request.urlopen(r, timeout=600) as resp: etags.append(resp.headers.get("etag"))
    http("https://api.linkedin.com/rest/videos?action=finalizeUpload",
         {"finalizeUploadRequest": {"video": v["video"], "uploadToken": v.get("uploadToken", ""), "uploadedPartIds": etags}}, li_h())
    return v["video"], None

def op_li_post(req):
    """{text, video_url? | image_url?} : one post on the TrueYards company page."""
    body = {"author": LI_ORG, "commentary": req.get("text", "")[:3000], "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "lifecycleState": "PUBLISHED", "isReshareDisabledByAuthor": False}
    if req.get("video_url"):
        urn, err = li_upload("videos", fetch(req["video_url"]))
        if err: return {"media_error": err}
        body["content"] = {"media": {"title": req.get("title", "TrueYards"), "id": urn}}
    elif req.get("image_url"):
        urn, err = li_upload("images", fetch(req["image_url"]))
        if err: return {"media_error": err}
        body["content"] = {"media": {"id": urn}}
    return http("https://api.linkedin.com/rest/posts", body, li_h())

def op_threads_comments(req):
    """{days?} : replies other people left on our recent Threads posts (with our existing answers)."""
    me = th("me", {"fields": "id,username"}, "GET")
    if "id" not in me: return {"auth_error": me}
    since = time.time() - int(req.get("days", 3)) * 86400
    posts = th(f"{me['id']}/threads", {"fields": "id,text,timestamp,permalink", "limit": 25}, "GET").get("data", [])
    out = []
    for m in posts:
        try:
            if datetime.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z").timestamp() < since: continue
        except Exception: pass
        cs = th(f"{m['id']}/conversation", {"fields": "id,text,username,timestamp,replied_to,is_reply_owned_by_me", "reverse": "false"}, "GET")
        for c in cs.get("data", []):
            c["post_id"] = m["id"]; c["post_text"] = (m.get("text") or "")[:120]; c["permalink"] = m.get("permalink")
            out.append(c)
    return {"username": me.get("username"), "comments": out}

def op_threads_reply(req):
    """{reply_to_id, text} : publish a reply under a Threads post or reply."""
    me = th("me", {"fields": "id"}, "GET")
    if "id" not in me: return {"auth_error": me}
    c = th(f"{me['id']}/threads", {"media_type": "TEXT", "text": req["text"][:500], "reply_to_id": req["reply_to_id"]})
    if "id" not in c: return {"container_error": c}
    th_wait(c["id"])
    return {"published": th(f"{me['id']}/threads_publish", {"creation_id": c["id"]})}

def op_ig_comments(req):
    """{post_urls:[...], per_post?:60} -> public comments on those posts (audience voice mining)."""
    inp = {"directUrls": req["post_urls"], "resultsLimit": int(req.get("per_post", 60))}
    j = http(f"https://api.apify.com/v2/acts/apify~instagram-comment-scraper/run-sync-get-dataset-items?token={E('APIFY_TOKEN')}&timeout=280", inp, timeout=320)
    if isinstance(j, dict): return {"error": j}
    keep = ("postUrl", "text", "ownerUsername", "likesCount", "timestamp", "repliesCount")
    return {"count": len(j), "comments": [{k: it.get(k) for k in keep} for it in j]}

OPS = {"ig_scan": op_ig_scan, "yt_short": op_yt_short, "yt_check": op_yt_check, "yt_stats": op_yt_stats,
       "threads_post": op_threads_post, "threads_refresh": op_threads_refresh, "x_post": op_x_post, "li_post": op_li_post,
       "threads_comments": op_threads_comments, "ig_comments": op_ig_comments, "threads_reply": op_threads_reply}

def scrub(o):
    s = json.dumps(o)
    for k in ("APIFY_TOKEN", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN", "THREADS_TOKEN", "X_API_SECRET", "X_ACCESS_SECRET", "X_ACCESS_TOKEN", "LI_TOKEN"):
        v = E(k)
        if v: s = s.replace(v, "***")
    return json.loads(s)

for f in sorted(glob.glob("social/requests/*.json")):
    name = os.path.basename(f)[:-5]
    if os.path.exists(f"social/processed/{name}"):
        os.remove(f); continue
    open(f"social/processed/{name}", "w").write(datetime.datetime.utcnow().isoformat())
    try:
        req = json.load(open(f)); fn = OPS.get(req.get("op"))
        res = fn(req) if fn else {"error": "unknown op"}
    except Exception as e:
        res = {"error": f"{type(e).__name__}: {e}"[:400]}; req = {}
    json.dump(scrub({"op": req.get("op"), "ran_at": datetime.datetime.utcnow().isoformat() + "Z", "result": res}), open(f"social/results/{name}.json", "w"), indent=1)
    os.remove(f); print("done", name)
