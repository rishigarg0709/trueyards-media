"""Gemini (Veo) video jobs for website visuals, added 27 Nov 2026 by the Google Ads and YouTube ads chat (pf.gads).
Each file in vjobs/*.json is a list of tasks; results land in library/web/<name>.mp4 and a log in library/web/_last_run.txt.
Kinds: "list" (writes every model name the key can use) and "veo" (image to video, optional last frame).
The key comes from the GitHub secret GEMINI_API_KEY only; nothing secret is printed or written."""
import base64, glob, json, os, sys, time, urllib.request, urllib.error

OUT = "library/web"; os.makedirs(OUT, exist_ok=True)
GM = os.environ.get("GEMINI_API_KEY", ""); BASE = "https://generativelanguage.googleapis.com/v1beta"
log = []

def call(url, body=None, method="POST", raw=False):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json", "x-goog-api-key": GM})
    with urllib.request.urlopen(r, timeout=600) as resp:
        b = resp.read()
        return b if raw else json.loads(b)

def list_models(t):
    rows, tok = [], ""
    while True:
        j = call(f"{BASE}/models?pageSize=200" + (f"&pageToken={tok}" if tok else ""), method="GET")
        rows += [f"{m['name']} | {','.join(m.get('supportedGenerationMethods', []))}" for m in j.get("models", [])]
        tok = j.get("nextPageToken")
        if not tok: break
    open(f"{OUT}/{t['name']}.txt", "w").write("\n".join(rows)); print("\n".join(r for r in rows if "veo" in r.lower())); return f"{len(rows)} models"

def _img(p):
    return {"bytesBase64Encoded": base64.b64encode(open(p, "rb").read()).decode(), "mimeType": "image/png" if p.endswith(".png") else "image/jpeg"}

def veo(t):
    model = t.get("model", "veo-3.1-generate-preview")
    inst = {"prompt": t["prompt"]}
    if t.get("image"): inst["image"] = _img(t["image"])
    if t.get("last_frame"): inst["lastFrame"] = _img(t["last_frame"])
    params = {"aspectRatio": t.get("aspect", "16:9")}
    for k_in, k_out in (("seconds", "durationSeconds"), ("resolution", "resolution"), ("negative", "negativePrompt")):
        if t.get(k_in): params[k_out] = t[k_in]
    op = call(f"{BASE}/models/{model}:predictLongRunning", {"instances": [inst], "parameters": params})
    name = op["name"]
    for _ in range(90):  # up to about 15 minutes
        time.sleep(10)
        op = call(f"{BASE}/{name}", method="GET")
        if op.get("done"): break
    if not op.get("done"): return "timed out: " + name
    if op.get("error"): return "error: " + json.dumps(op["error"])[:300]
    resp = op.get("response", {})
    samples = (resp.get("generateVideoResponse") or resp).get("generatedSamples") or resp.get("generatedVideos") or []
    if not samples: return "no video: " + json.dumps(resp)[:300]
    uri = (samples[0].get("video") or {}).get("uri")
    data = call(uri, method="GET", raw=True)
    open(f"{OUT}/{t['name']}.mp4", "wb").write(data)
    os.makedirs("ops", exist_ok=True)
    with open("ops/veo_spend.jsonl", "a") as f:
        f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "model": model, "seconds": params.get("durationSeconds", 8), "by": t.get("by", "")}) + "\n")
    return f"video ok {len(data)} bytes"

KINDS = {"list": list_models, "veo": veo}
for f in sorted(glob.glob("vjobs/*.json")):
    for t in json.load(open(f)):
        try: msg = KINDS[t["kind"]](t)
        except urllib.error.HTTPError as e: msg = f"HTTP {e.code}: {e.read()[:300]!r}"
        except Exception as e: msg = f"ERR {e!r}"[:300]
        log.append(f"{t.get('name')} [{t['kind']}]: {msg}"); print(log[-1])
    os.remove(f)
open(f"{OUT}/_last_run.txt", "w").write(time.strftime("%Y-%m-%d %H:%M UTC\n", time.gmtime()) + "\n".join(log))
