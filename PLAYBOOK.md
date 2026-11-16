# TrueYards daily posting playbook

Owner: Rishi Garg. Goal he set: 1 million organic followers on Instagram within a year. Page: instagram.com/trueyards.in (Instagram account id 17841429830946947, connected in Windsor.ai). Positioning: India's property and money, explained with data. Education only, not advice. Entirely organic. Not a Forteasia or Haryana promotion page: never post Forteasia projects, FIT, prices of specific projects or sales calls here.

## What wins reach (researched Nov 2026)
- Instagram ranks on watch time, likes per reach and sends per reach. Sends (DM shares) matter most for reaching non-followers. Design every post so a viewer thinks "I must send this to X".
- Originality: only original content gets recommended. Build every chart and slide from primary data. Never repost or screenshot other creators or news graphics.
- Carousels: cover hook in 10 words or fewer; slide 2 must work as a standalone hook (Instagram re-serves unswiped carousels from slide 2); one idea per slide; 7 to 10 slides (Windsor allows at most 10); a recurring visual element that crosses slide edges to pull the swipe; end with a send prompt naming a specific person.
- Hashtags: at most 5, specific. Put search keywords (city names, terms people type) in the first caption line and body.
- High-arousal emotions (awe at a number, anxiety about a trap, with the fix) and practical utility drive sharing. Avoid tribal outrage.

## Content pillars (rotate; aim for variety, never the same look two days running)
1. City price check: what money buys, years of salary to afford a home, rents, yields.
2. Home loan and EMI maths: tenure, prepayment, rate changes, total interest.
3. Buyer protection: documents, RERA checks, clauses, carpet vs super area, hidden costs, scams.
4. Money basics: salary in-hand, tax with a home loan, capital gains, stamp duty by state.
5. Infrastructure and city futures: expressways, metros, airports, industrial corridors (facts and history only, no "prices will rise" claims).
6. Myths and debates: rent vs buy, "property never falls", real estate vs other assets using official historical data.
7. Data stories from the latest reports (RBI, NHB RESIDEX, Knight Frank, Anarock, PropTiger, CBRE, JLL, Colliers, Vestian, MoSPI).

Seasonal overrides: Union Budget (1 Feb), RBI policy days, ITR season (July), festive season.

## Compliance (hard rules)
- Education only. No buy, sell or hold calls on stocks, funds or specific properties. No return promises or predictions ("will double", "best time to buy").
- SEBI: do not use market prices of named securities from the last three months.
- Every number needs a named source and date on the slide or in the caption. If a number cannot be verified from a primary or reputable source found in this run, do not use it.
- Label AI-generated imagery ("AI-generated imagery" in the footer). Never present AI renders as real places or projects.
- No em dashes anywhere (slides or captions). Plain, direct, MBA-appropriate tone. No hype words.
- Footer on every slide: short disclaimer, e.g. "Educational content, not advice. Source: ...".

## Brand and design
- Logo: TrueYards wordmark ("True" in ink or white, "Yards" in green #2f9f78 on light or #5cc49c on dark) with the green square Y mark. Header on every slide: wordmark top left, "NN / NN" counter top right.
- Size: 1080 x 1350 (4:5). Render at 2x and downscale to 1080 x 1350 JPEG (quality 90) before publishing. Keep key text inside the central 3:4 area. Body text at least 28 px at 1080 width.
- te.html: bone and green 'follow the loan' story (Outfit thin lowercase, green #1f7a5a, a data curve running across slides 3 to 7, model photographs cut across slide boundaries, ghost year numerals). Made 14 Nov; this is the current reference for quality.
- td.html: midnight navy data story (Rishi found it dull: flat stat list, render-look images, no cross-slide cut; do not repeat that) (Outfit thin lowercase, amber #ffb454, 3D model images generated on navy). Made 14 Nov for the under 50 lakh post.
- Three proven looks live in engine/templates (study them, then make new variations; do not copy one every day):
  - ta.html: warm cream editorial (Outfit thin lowercase headlines, one red accent #e2452b, a ruler running under all slides). Use for money maths.
  - tb.html: deep green poster (Anton caps, red tape with numbered seals, still-life photos). Use for checklists and buyer protection.
  - tc.html: near-black data story (Space Grotesk, orange #ff6a1a data accents, cinematic photos, source ticker). Use for data and reports.
- New looks are welcome when they fit the topic, but keep the TrueYards header so the feed stays recognisable. Rishi's taste: premium, simple, quiet, typographic, real depth and layering; he dislikes cheap template looks, clutter, clipped letters and "AI slop". Mixed case and thin weights are liked; he disliked a serif italic accent (Fraunces) and preferred Jost italic for small accent lines.
- Imagery (Rishi's rule: "I want these type of posts only"): every post must carry photo-style imagery at the level of the three launch carousels. No text-only or chart-only carousels. At least 3 slides, including the cover, have a photographic image blended into the design. Sources, in library/README.md: (1) library/gen, 3D images generated fresh for today's story through the gen/ workflow, which is the default and should supply at least 2 images per post; (2) library/ai, the hand-picked Gemini stock, best for full-bleed covers; (3) real photos fetched from Unsplash into library/stock. Label AI images. Do not use photos of identifiable people or public figures, news agency photos, or anything copied from other sites.
- How images are blended (this is what makes it look edited, not templated): never drop a photo in a plain rectangle. Match the photo's background to the slide colour (still lifes on cream or green sit directly on the same colour), feather the edges with gradient masks (see the nested mask wrappers in the templates), let one image run across a slide boundary, add a subtle gradient under text, and grade real photos to the palette (darken and cool for tc, warm and soften for ta) with CSS filters.

## The daily run
1. Read this file and log.md. Check what was posted recently so topics and looks rotate.
2. If queue/ has a folder, publish the oldest one (skip to step 6). Otherwise make a new post (steps 3 to 5).
3. Pick the topic: today's news first (RBI, budget, a fresh report), else the next pillar in rotation. Research with web search; gather every figure with its source and date. Then make the images: write 3 to 5 story-specific 3D image prompts in the house style and generate them with variants through the gen/ workflow, and add library/ai or Unsplash photos where they fit better (library/README.md has the steps).
4. Design: write an HTML page that is one continuous canvas, N x 1080 px wide and 1350 px tall (N = 7 to 10), elements with class "t" for text. Render with `node engine/multi.cjs <file.html> N 2`, slice with `python3 engine/slice.py <file.png> N <name> <outdir>` (writes <name>-slide-K.jpg at 2160 x 2700 and a contact sheet <file>-sheet.jpg). Look at the contact sheet and at least two slides at full size. Fix clipped text, overlaps, empty areas and edge issues (multi.cjs prints "EDGE" lines for text too close to a slide edge). Downscale slides to 1080 x 1350 JPEG.
4a. Quality gate (do not skip). Open the launch reference slides posts/2026-11-14-carpet-area/slide-1.jpg and slide-3.jpg, then open every new slide at full size next to them. Publish only if all are true: (1) the cover would stop a scroll and reads in under 2 seconds; (2) images are blended with no visible box edges, no stretched or pixelated photos, no watermark; (3) no clipped, overlapping or orphaned text, no EDGE warnings; (4) every slide has one idea and clear hierarchy; (5) nothing looks like a stock template; (6) every figure has a source. Fix and re-render up to 3 rounds. If it still falls short, do not publish it: publish the oldest folder in queue/ instead, or if the queue is empty, skip the day and tell Rishi in one line. A missed day is better than a weak post.
5. Write caption.txt: first line restates the hook with keywords; short body; a send prompt naming who to send it to; the source line; the disclaimer; at most 5 hashtags. Under 2,200 characters.
6. Move/copy the slides to posts/<YYYY-MM-DD>-<slug>/slide-1.jpg ... and caption.txt. Commit and push to main. Raw URLs: https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/posts/<folder>/slide-K.jpg. Wait about 30 seconds after pushing.
7. Publish with Windsor.ai: connector "instagram", action "create_carousel_post", account "17841429830946947", params {image_urls: [...in order...], caption}. If it fails because an image cannot be fetched, wait a minute and retry once.
8. Append a row to log.md (include the image files used) and push.
9. Final message for Rishi (pushed to his phone): first line bold "TrueYards post live, <date>", then the title, one line on why this topic, and a reminder to add a music track from his phone (carousels with music reach more; the API cannot attach music). No em dashes.

## Limits
- Windsor free plan: only this Instagram account is connected; the Facebook Page is not. Turn on Instagram's "share to Facebook" in the app for cross-posting.
- Max 10 images per carousel through the API.
- If Windsor reports the account disconnected or write actions disabled, stop and tell Rishi in one line.

## Reels: hook and style rules (Rishi feedback, 15 Nov 2026)
- The first 1 to 3 seconds decide everything. Never open on a slow word reveal over a still. Frame 0 must already show the core tension (a big number, a before/after, a contradiction), with motion from the first frame.
- Land the payoff of the hook on the music drop at about 1.5 s (flash, shake, impact), then a curiosity line by second 3.
- Story reels: one short sentence per screen, held long enough to read; one recurring device carries the story (countdown, year counter, price tag).
- Rotate visual styles. Do not reuse the same palette and fonts reel after reel. Styles so far: "Bone/Red 3D" (Mumbai), "Ledger Noir" black/ivory/saffron with Fraunces + Space Grotesk + Plex Mono (Gurgaon).
- Music: catchy, beat-forward tracks (hip hop, phonk, desi). Rishi rejected dark ambient underscores and orchestral hip hop. Offer 2 to 3 track previews of the hook when unsure.

## Voiceover reels (16 Nov 2026)
- Narrator: ElevenLabs voice "Jessa - Easygoing and Effortless" (voice_id yj30vwTGJxSHezdAGsv9), model eleven_v3. Rishi picked it as the most natural.
- Humanise scripts: short sentences, "..." and [short pause]/[pause] tags, a question to the viewer at the end. Trim any pause longer than 0.4 s in the edit.
- Every on-screen word reveals at its spoken timestamp (alignment from /with-timestamps). Frame 0 shows the full hook statement before the voice says it.
- Music: ElevenLabs Music bed per reel, ducked about 10 dB under the voice, lifting in pauses.
- Cloud jobs: push a JSON list to jobs/*.json (kinds: voice, music, image, shared, addvoice, voices, models); results land in library/media/.
- Style 3 "Height Ruler": cream/black/TrueYards green, Inter 900 + Plex Mono, block-column wipes, a persistent ruler device. Used for the Delhi skyscrapers reel.

## Hooks and virality
Full rulebook: REEL_HOOKS_PLAYBOOK.md. Every reel must pass its frame-0 test and pre-publish checklist.
