# Reel pipeline (how a daily reel gets made)

Channel: TrueYards, "Real Estate Explained!" Everything about real estate: city mysteries, stories, history, money, rules, global comparisons, news explained, marvels, builders' stories, weird facts, myth vs fact. About 70% India, 30% global. Education only.

Before anything else, read REEL_HOOKS_PLAYBOOK.md (the rules) and look at the reference reel `reels/2026-11-16-delhi-skyscrapers/` (Rishi approved it as the quality bar; the posted version is `drafts/delhi-skyscrapers-reel/reel.mp4`).

## Setup (fresh session)
- `cd engine && npm install` (fonts). Playwright at /opt/npm-tools/node_modules/playwright (set env PW to another path if needed).
- `pip install --break-system-packages librosa soundfile numpy pillow` if missing. ffmpeg must exist.

## Steps
0. **Tonight's plan first.** If plans/<today>/<slot>/plan.md exists (slot = midday, evening or carousel), the nightly prep run already claimed the topic, verified facts, wrote the script and ordered the images by half-price batch. Use that plan and the images it lists in library/media/. If any listed image is missing at run time (check batches/failed/ and batches/pending/), generate only the missing ones with the normal image job. If no plan exists, do the full pipeline below.
   **Image cost rules (always):** (a) get 2 to 3 shots from each image (use its upscaled `-4k.jpg`) by cropping and moving (wide, push-in on a detail, pan); never crop below 2160 px wide; (b) use real free photos (Wikimedia Commons, Unsplash via fetch/*.txt) for real named places and history, credited in the caption; (c) reuse matching images already in library/ai, library/media and library/gen for generic shots; (d) use the look's prompt template in STYLE_SYSTEM.md so images do not need redoing. Target at most 6 new generated images per reel and 5 per carousel (carousels must stay visually rich, see PLAYBOOK.md Brand and design).
1. **Style.** Read STYLE_SYSTEM.md. Pick one look and one voice for the reel (different look from the previous reel; rotate voices) and follow its editing standard.
   **Learnings first.** Read learnings/VIRALITY_PLAYBOOK.md (publish gate, hook library, topic mix) and learnings/LEARNINGS.md and follow its Do more / Do less and running experiments when picking the topic, hook archetype, length and style. Log the look letter, voice name, hook archetype (number from the hook library), format, pillar, India or global, language, length, accent, music style and the send-test answer in log.md so the analytics run can score them.
   **Topic.** Take the first unchecked topic in `queue/reel-topics.md` whose pillar differs from the last 2 reels in log.md (a big news story can jump the queue). Mark it `[x]` with the date when published. When fewer than 10 remain, add 15 new scored topics across the pillars.
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
7. **Cover (mandatory, keeps the profile grid uniform).** Make a designed cover with the house template: write a spec JSON {image (the reel's best hero image, absolute path), focus (CSS background-position), kicker (2 to 4 words, e.g. city or series), title (the hook in 2 lines, at most about 6 words, with the key words in <mark>), accent (the reel's accent colour)} and run `node scripts/reel/cover.cjs spec.json drafts/<slug>/cover.jpg`. It must print no WARN. Look at it, and at its 3:4 centre crop (y 240 to 1680), which is how the profile grid shows it. Every reel uses this same layout so the grid looks like one brand.
8. **Publish (Meta bot).** Copy the mp4 to `drafts/<slug>/reel.mp4` with `caption.txt` and `cover.jpg` and push. Then push these request files together in meta/requests/ (see PLAYBOOK.md "Meta bot publishing"):
   - `<date>-<slot>-ig.json` {"op":"ig_reel","video_url":<raw URL>,"cover_url":<raw URL of cover.jpg>,"caption":...,"share_to_feed":true}
   - `<date>-<slot>-fb.json` {"op":"fb_reel","video_url":<raw URL>,"description":<same caption>}
   When the Instagram result shows the media id, push `<date>-<slot>-story.json` {"op":"ig_story","image_url":<raw URL of cover.jpg>} so followers see a story pointing to the new reel.
   **Trial twin (midday slot only):** render a second cut that changes only the first 3 to 5 seconds (a different hook archetype from the library: new first line of voiceover and new opening visual; the rest identical), save it as `drafts/<slug>/reel-trial.mp4`, and publish it with {"op":"ig_reel","video_url":...,"caption":...,"trial":true}. Log both in log.md as a pair (main hook vs trial hook) so the learning run can compare them on skip rate and hold. If the trial result shows an eligibility error, skip trials and note it in log.md.
   **Cross-post (after Instagram succeeds):** push social/requests/<date>-<slot>-yt.json {"op":"yt_short","video_url":<raw URL>,"title":<hook line, under 90 chars>,"description":<caption>,"tags":[3 to 6 topic words],"privacy":"public"}, <date>-<slot>-threads.json {"op":"threads_post","video_url":<raw URL>,"text":<caption shortened to 500 chars>} and <date>-<slot>-x.json {"op":"x_post","video_url":<raw URL>,"text":<hook line plus one fact, under 270 chars>} in one push; read social/results/. If a result says auth_error or a key is missing, skip that platform and note it in log.md (Rishi may not have connected it yet). Do not cross-post trial twins.
   Fallback only if the Meta bot result shows an error for Instagram: Windsor `execute_action` connector "instagram", action "create_video_post", account "17841429830946947", params {video_url, cover_url, caption, share_to_feed: true}.
   Append to log.md: date, REEL, title, media id (and trial media id), look, voice, hook archetype, story type, accent, music style.

## Style rules that Rishi set
- Realistic and professional, documentary look. Photoreal AI images or real photos, slow camera moves, clean lower-third text, thin news-style callouts, one decisive visual event in the hook. No cartoon or game-style 3D.
- One accent colour per reel (red or green or another single accent) with white. The TrueYards logo is never recoloured: `library/brand/trueyards-icon.png` + "True" white/ink + "Yards" #28c39d.
- No dark boxes behind captions; use gradients and text shadow, or highlight blocks on key words.
- Music must be catchy and beat-driven; downbeat on the hook's key word, cuts on beats.
- Vary visual style between consecutive reels (fonts, accent, layout), keep quality constant.

## ElevenLabs credit budget (Creator plan: 131,000 credits a month, resets on the 16th)
- Budget per reel: about 1,600 credits (voiceover about 800, music about 700 for 45 s). 60 reels a month is about 96,000, leaving room for retries and the weekly music reel.
- Voice: write the final script before generating; at most one regeneration per reel.
- Music: generate 45 s, not longer. Save every good track to library/music/<look>/ with its BPM; reuse a saved track for the same look instead of generating when one fits.
- Before generating, run the usage job ({"kind":"usage","name":"el-usage"}). If used credits exceed the share of the month passed plus 10% (for example over 60% by day 15), reuse library music for that reel.

## Quality standard: 4K masters, best-accepted export per platform (16 Nov 2026)
Everything is made at 4K-class resolution and each platform gets the highest version its API accepts.

| Asset | Master | Instagram / Facebook / Threads / LinkedIn | YouTube | X |
|---|---|---|---|---|
| Reel | `reel-4k.mp4` 2160x3840, CRF 14 (local only) | `reel.mp4` 1440x2560, ≤24 Mbps | `reel-yt.mp4` 2160x3840 (plays in 4K) | `reel-x.mp4` 1068x1900 |
| Reel cover | `cover.jpg` 2160x3840 | `cover-ig.jpg` 1440x2560 | `cover.jpg` | n/a |
| Carousel slide | `master/*-slide-N.jpg` 2160x2700 | `*-slide-N.jpg` 1440x1800 | n/a | 1440x1800 |
| AI images | Gemini at 2K, then free Real-ESRGAN upscale to `<name>-4k.jpg` (2x) | | | |

Rules
- Frames render at deviceScaleFactor 2 (1080 layout, 2160x3840 pixels). `SCALE=1` only for drafts, never for publishing.
- Meta's API rejects reels wider than 1920 px or above 25 Mbps and images wider than 1440 px, and Instagram streams at about 1080p anyway. Uploading 1440 wide downscaled from a 4K master gives the sharpest result Instagram will show.
- Source photos must be at least 3840 px on the long edge. Gemini images: use `library/media/<name>-4k.jpg` (made automatically by scripts/upscale.py after every image job, no API cost). Any other small image: run `python3 scripts/upscale.py <file>`. Unsplash: full-size download. Never stretch a small image.
- Every upload file is capped under 95 MB so it can be served from GitHub raw URLs (100 MB limit); the archival master stays local.
- Encode: H.264 High, level 5.1, closed GOP (2 s), 30 fps, yuv420p, AAC 48 kHz. Master `-preset slow`.
- Check before publishing: `ffprobe` each export for width, height and bitrate; look at one full-size still for soft text or blur.
