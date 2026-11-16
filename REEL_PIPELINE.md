# Reel pipeline (how a daily reel gets made)

Channel: TrueYards, "Real Estate Explained!" Everything about real estate: city mysteries, stories, history, money, rules, global comparisons, news explained, marvels, builders' stories, weird facts, myth vs fact. About 70% India, 30% global. Education only.

Before anything else, read REEL_HOOKS_PLAYBOOK.md (the rules) and look at the reference reel `reels/2026-11-16-delhi-skyscrapers/` (Rishi approved it as the quality bar; the posted version is `drafts/delhi-skyscrapers-reel/reel.mp4`).

## Setup (fresh session)
- `cd engine && npm install` (fonts). Playwright at /opt/npm-tools/node_modules/playwright (set env PW to another path if needed).
- `pip install --break-system-packages librosa soundfile numpy pillow` if missing. ffmpeg must exist.

## Steps
1. **Topic.** Take the first unchecked topic in `queue/reel-topics.md` whose pillar differs from the last 2 reels in log.md (a big news story can jump the queue). Mark it `[x]` with the date when published. When fewer than 10 remain, add 15 new scored topics across the pillars.
2. **Research.** Verify every number and claim from primary or reputable sources found today. Keep a source list for the caption. If a fact can't be verified, drop it.
3. **Script.** 35 to 55 s of narration (about 110 to 150 words). Hook line states the conflict by 1.5 s. Open loop early, escalate, pay off, end on a pick-a-side question. Short sentences, `...` and `[short pause]` for natural rhythm. No em dashes.
4. **Cloud jobs** (push one JSON file to `jobs/`, the GitHub workflow runs it in 1 to 3 minutes; results land in `library/media/`, log in `library/media/_last_run.txt`):
   - voice: `{"kind":"voice","name":"<slug>-vo-1","voice_id":"yj30vwTGJxSHezdAGsv9","model":"eleven_v3","text":"...","settings":{"stability":0.5,"similarity_boost":0.8,"style":0.3,"use_speaker_boost":true}}`. Make 2 takes, pick the one whose hook word lands earliest.
   - music: `{"kind":"music","name":"<slug>-beat","prompt":"<style> instrumental at exactly 96 BPM in 4/4 ... starts immediately with the full beat, strong clear downbeats, no vocals","ms":62000}`. Vary style per reel (documentary hip-hop, cinematic trap, lo-fi house, tense orchestral-hybrid with drums), always a steady beat.
   - images: `{"kind":"image","name":"<slug>-x","prompt":"Photorealistic ... vertical 9:16 ... no text, no logos, no people visible"}` (Gemini, about ₹11 each, keep to 6 or fewer per reel). For an edit of an existing image add `"inputs":["library/media/<file>.png"]`. Real photos of named real places: Unsplash or Wikimedia Commons via `fetch/*.txt` (see library/README.md), credited.
5. **Build.** `cp -r reels/2026-11-16-delhi-skyscrapers reels/<date>-<slug>`, replace `img/` with this reel's images, then:
   - `python3 scripts/reel/vo_align.py library/media/<vo>.mp3 library/media/<vo>.align.json reels/<dir>` (vo.wav + words.json)
   - `python3 scripts/reel/beats.py library/media/<beat>.mp3 <hook_word_time> reels/<dir>/beats.json`
   - Rewrite the scenes in `reel.html`: keep the engine (helpers, `at()`, `T()`/`rv()` word reveals, block wipe, logo, fine print, ruler if useful, beat snapping `SN`) and write new `add(t, scene)` blocks for this story. Paste the new words.json into `const WS=` and beats into `const BEATS=`. Update `FINE` (sources, AI labels, photo credits) and the end card.
   - Write `hits.json` (a boom on the hook's key word, whooshes on big cuts).
   - Stills check: `node scripts/reel/shot.cjs reels/<dir> stills 0 0.5 1.5 3 ...` and LOOK at every still at full size: frame-0 test, text readable on its worst frame, nothing behind the logo, safe zones (top 250 px, bottom 400 px clear of key text).
   - `python3 scripts/reel/mix.py reels/<dir> library/media/<beat>.mp3` then `scripts/reel/render.sh reels/<dir>`.
6. **QA** with the playbook checklist. Watch for: hook lands by 1.5 s, visual change at least every 3 s, single accent colour, real logo, facts sourced. Up to 3 fix rounds; if still weak, do not publish (say so).
7. **Publish.** Copy the mp4 to `drafts/<slug>/reel.mp4` with `caption.txt`, push, wait about 30 s, then Windsor `execute_action` connector "instagram", action "create_video_post", account "17841429830946947", params {video_url: raw.githubusercontent.com URL, caption, share_to_feed: true, thumb_offset: 300}. Append to log.md: date, REEL, title, media id, pillar, hook archetype, accent colour, music style.

## Style rules that Rishi set
- Realistic and professional, documentary look. Photoreal AI images or real photos, slow camera moves, clean lower-third text, thin news-style callouts, one decisive visual event in the hook. No cartoon or game-style 3D.
- One accent colour per reel (red or green or another single accent) with white. The TrueYards logo is never recoloured: `library/brand/trueyards-icon.png` + "True" white/ink + "Yards" #28c39d.
- No dark boxes behind captions; use gradients and text shadow, or highlight blocks on key words.
- Music must be catchy and beat-driven; downbeat on the hook's key word, cuts on beats.
- Vary visual style between consecutive reels (fonts, accent, layout), keep quality constant.
