# FIT Reel 03: voiceover ad reel (17 Nov 2026)

Paid-ad reel for the FIT click-to-WhatsApp campaign (not for the TrueYards organic feed). 31 s, 1080x1920, two versions with the same visuals:
English VO (fit-r3-vo-en-1) and Hindi VO (fit-r3-vo-hi-1), ElevenLabs voice yj30vwTGJxSHezdAGsv9, eleven_v3; music fit-r3-beat (100 BPM, ElevenLabs). All in library/media.

Built on the Reel 02 v2 engine (laptop: creative/reel02/fit-reel-02-v2-source.zip): search-bar hook "Land for my factory", real site footage in black and white, FIT red #E81C24, Barlow Condensed captions, HRERA numbers and a footage label on every frame, HRERA card, WhatsApp end card ("Tap the WhatsApp button below").
Every caption word appears when the voice says it (mkcfg.py reads the VO word timings).

Rebuild (needs the reel02 footage clips, fit_rev.png and fort_white.png from fit-creative-studio.zip, npm fonts barlow-condensed, ibm-plex-mono, hanken-grotesk):
1. `python3 scripts/reel/vo_align.py library/media/fit-r3-vo-en-1.mp3 library/media/fit-r3-vo-en-1.align.json ../en-1 0.3` (same for hi-1)
2. `python3 mkcfg.py` (scene and shot plan per language)
3. `python3 track3.py en`, overlay frames `node ovrender3.cjs <a> <b> cfg-en.json en` in chunks, `python3 mix3.py en`
4. ffmpeg overlay + mix (crf 19, max 10 Mbps, AAC 48 kHz), about -13 LUFS.

Footage notes: real-gate2 and real-gate3 have the source video's subtitles burned in, and real-aerial2 starts on a title card for 1 s: do not use those parts. AI clips only in scenes labelled "Representational model".
Brand pronunciation used in the VO: "Forte-Asia" (confirm with Rishi).
