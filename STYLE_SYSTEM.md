# TrueYards style system: looks, voices, editing standard

Rishi (2026-11-16): try different reel styles, colour tones and 2 to 3 voices, all ultra professional, "100k dollar editor" quality.
Each reel uses ONE look from start to end (Rishi's earlier rule: one theme per video). Rotate looks and voices across reels and log both in log.md so the analytics run can compare them. Logo rules never change: library/brand/trueyards-icon.png with "True" white and "Yards" #28c39d, never recoloured; every look keeps the top 300 px dark enough for it.

## Looks (pick the one that suits the story; do not repeat the same look twice in a row)
| Look | Palette | Image grade (put in the Gemini prompt) | Type | Music | Best for |
|---|---|---|---|---|---|
| A. Newsroom Red | near-black, white, one red #E63B2E | high-contrast documentary photo, cool shadows, slight film grain | Inter 900 caps headlines, mono kickers | tense percussion, 90 to 100 BPM | rules, scams, investigations, Twin Towers type stories |
| B. Emerald Doc | deep green-black, white, #28c39d | natural daylight, soft haze, National Geographic feel | Inter 800, serif accent for dates (Fraunces) | cinematic strings plus pulse | history, cities, planning stories |
| C. Midnight Gold | navy #0B1426, ivory, amber #F2B33D | blue hour, warm practical lights, glossy architecture | Inter 900 plus thin numerals | epic hybrid trailer, 100 to 120 BPM | marvels, megaprojects, money, luxury |
| D. Archive Sepia | warm black, paper cream text, oxblood #8C2F2B stamps | aged photo, sepia split-tone, paper texture, map overlays | Fraunces display plus mono captions | piano and low strings, ticking clock | old history, timelines, how cities began (Mumbai seven islands) |
| E. Blueprint | ink blue #0C2340, white line work, cyan #4FD1FF | technical render, section cuts, wireframe overlays on real images | Inter 700 with mono labels and dimension lines | minimal electronic, clean pulse | how it works, engineering (Burj Khalifa on sand), money breakdowns |
| G. Bold Type (carousels) | off-white #EEF1EA, one deep green #0E6B50, one reversed green slide | no images: giant type only | Anton display (free), Inter for labels and context | n/a | glossaries, myth vs fact, number shocks, checklists; reference posts/sample-bold-type |
| H. Explained to a beginner (carousel series) | white, deep green #0E6B50, mint #28c39d, coral #FF6B57 | clean editorial illustration with recurring original character Aarav (reference library/media/cs-aarav-solo.png, always pass it as input) | Inter 500/800, 2 to 3 centred lines on top, big illustration below | n/a | one real estate concept told as one everyday metaphor story, 8 to 12 slides, weekly; reference posts/sample-story-carousel |
| F. Tokyo Neutral | off-black, white, one soft coral #FF6B57 | quiet minimal photography, muted colours, lots of negative space | Inter 600, generous spacing | lo-fi or ambient beat | global comparisons, calm counterintuitive stories (Japan houses) |

Rules for every look: one accent colour only; text must read on its worst frame (darken or blur the area behind text inside the image, never a solid dark box behind captions); no gradients as decoration; label AI visuals "AI visualisation" in small type.

## Voices (rotate; log which one)
| Voice | ElevenLabs id | Character | Use for |
|---|---|---|---|
| Jessa | yj30vwTGJxSHezdAGsv9 | easygoing American, conversational | weird facts, global, light stories |
| George | JBFqnCBsd6RMkjVDRZzb | warm British documentary storyteller | history, marvels, slow-burn stories |
| Tara (TY Tara) | P7vsEyTOpZ6YUTulin8m | expressive Indian English, actress | India rules, money, NCR and Indian city stories, dramatic stories |

Rishi's final pick (2026-11-16): Jessa, George and Tara only. Do not use Viraj, Riya or Monika.
Model eleven_v3. Use v3 delivery tags sparingly ([pause], [whispers] on a secret, [excited] on a reveal). Never clone a real person's voice.

## Editing standard (applies to every look)
1. Frame 0 is already moving: a push-in, a reveal, or an object in motion. Never a static title card.
2. Every shot moves: slow push-in or pull-out (2 to 6% scale over the shot), or parallax by splitting foreground and background layers. Vary direction shot to shot.
3. Cuts land on beats (snap within 0.2 s); hits on reveals; one bigger music drop on the hook word and one at the payoff.
4. Transitions are motivated: match cuts (shape to shape), whip pans on fast beats, mask wipes along a building edge or road, zoom-through into the next shot. Max one flashy transition per 10 s; plain cuts otherwise.
5. Kinetic typography: words appear as they are spoken (word-timed), key number counts up or slams in, one idea per card, 6 to 8 words max.
6. Data and maps: animated counters, map zoom from space to street, route lines drawing on, bars growing in sync with the voice.
7. Speed ramps: ease in and out on camera moves; a short hold (0.4 s) on the reveal frame.
8. Sound design: whoosh on transitions, low boom on reveals, riser into the payoff, subtle room tone; music ducked about 9 dB under voice; loudness about -14 LUFS.
9. Finish: light film grain and gentle vignette matched to the look; consistent colour grade across all images in the reel (same prompt grade words, same seed style).
10. Pacing: a new visual every 1.5 to 3 s, a mini-reveal every 5 to 8 s, the last line loops back to frame 0.
11. QA before publish: check the 5 busiest frames at full size (text readable, nothing overlapping the logo or the Instagram UI zones: keep text out of the bottom 320 px and right 140 px), audio peaks, and the cover crop (y 240 to 1680).

## Image prompt templates (append the look's grade line to every Gemini prompt for that reel)
- A Newsroom Red: "photorealistic documentary photograph, high contrast, cool desaturated shadows, overcast or dusk light, subtle 35mm film grain, shot on a full-frame camera, natural lens, no text, no logos, no watermarks"
- B Emerald Doc: "photorealistic National Geographic style photograph, soft natural daylight, gentle atmospheric haze, rich greens and earth tones, crisp detail, no text, no logos"
- C Midnight Gold: "photorealistic architectural photograph at blue hour, deep navy sky, warm amber practical lights, glossy reflective surfaces, long-lens compression, no text, no logos"
- D Archive Sepia: "aged archival photograph look, sepia split-tone, soft paper texture, slight vignette and dust, period-accurate details, no modern objects, no text"
- E Blueprint: "photorealistic engineering cutaway render, clean studio light, technical section view, subtle cyan accent light, high detail, no text labels"
- F Tokyo Neutral: "quiet minimal photograph, muted natural colours, soft even light, lots of negative space, calm composition, no text, no logos"
Composition for every image: vertical 9:16 at 2K, main subject in the middle third, empty calmer area in the lower third for captions, top 300 px darker for the logo. Ask for wide framing so 2 to 3 crops can be cut from one image.
