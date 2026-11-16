"""Cloud media jobs: ElevenLabs voice (with word timings), ElevenLabs music, Gemini images.
Each job file in jobs/*.json is a list of tasks; results land in library/media/<name>.*
and a log in library/media/_last_run.txt. Keys come from GitHub secrets only."""
import base64, glob, json, os, sys, time, urllib.request, urllib.error

OUT = "library/media"; os.makedirs(OUT, exist_ok=True)
EL = os.environ.get("ELEVENLABS_API_KEY", ""); GM = os.environ.get("GEMINI_API_KEY", "")
log = []

def req(url, body=None, headers=None, method="POST", raw=False):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(r, timeout=300) as resp:
        b = resp.read()
        return b if raw else json.loads(b)

def voice(t):
    vid = t.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
    body = {"text": t["text"], "model_id": t.get("model", "eleven_multilingual_v2"),
            "voice_settings": t.get("settings", {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True})}
    j = req(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", body, {"xi-api-key": EL})
    open(f"{OUT}/{t['name']}.mp3", "wb").write(base64.b64decode(j["audio_base64"]))
    json.dump(j.get("alignment"), open(f"{OUT}/{t['name']}.align.json", "w"))
    return "voice ok"

def music(t):
    body = {"prompt": t["prompt"], "music_length_ms": int(t.get("ms", 45000)), "model_id": t.get("model", "music_v1")}
    if t.get("instrumental", True): body["force_instrumental"] = True
    b = req("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", body, {"xi-api-key": EL}, raw=True)
    open(f"{OUT}/{t['name']}.mp3", "wb").write(b); return f"music ok {len(b)} bytes"

def voices(t):
    j = req("https://api.elevenlabs.io/v1/voices", None, {"xi-api-key": EL}, method="GET")
    rows = [f"{v['voice_id']} | {v['name']} | {json.dumps(v.get('labels', {}))}" for v in j.get("voices", [])]
    open(f"{OUT}/{t['name']}.txt", "w").write("\n".join(rows)); return f"{len(rows)} voices"

def image(t):
    model = t.get("model", "gemini-3-pro-image-preview")
    body = {"contents": [{"parts": [{"text": t["prompt"]}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": t.get("aspect", "9:16"), "imageSize": t.get("size", "2K")}}}
    j = req(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", body, {"x-goog-api-key": GM})
    for p in j["candidates"][0]["content"]["parts"]:
        d = p.get("inlineData") or p.get("inline_data")
        if d:
            open(f"{OUT}/{t['name']}.png", "wb").write(base64.b64decode(d["data"])); return "image ok"
    return "no image: " + json.dumps(j)[:300]

def models(t):
    j = req("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", None, {"x-goog-api-key": GM}, method="GET")
    rows = [m["name"] for m in j.get("models", []) if "image" in m["name"]]
    open(f"{OUT}/{t['name']}.txt", "w").write("\n".join(rows)); return f"{len(rows)} image models"

KINDS = {"voice": voice, "music": music, "voices": voices, "image": image, "models": models}
for f in sorted(glob.glob("jobs/*.json")):
    for t in json.load(open(f)):
        try: msg = KINDS[t["kind"]](t)
        except urllib.error.HTTPError as e: msg = f"HTTP {e.code}: {e.read()[:300]!r}"
        except Exception as e: msg = f"ERR {e!r}"[:300]
        log.append(f"{t.get('name')} [{t['kind']}]: {msg}"); print(log[-1])
    os.remove(f)
open(f"{OUT}/_last_run.txt", "w").write(time.strftime("%Y-%m-%d %H:%M UTC\n", time.gmtime()) + "\n".join(log))
