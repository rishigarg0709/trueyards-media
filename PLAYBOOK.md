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
- Three proven looks live in engine/templates (study them, then make new variations; do not copy one every day):
  - ta.html: warm cream editorial (Outfit thin lowercase headlines, one red accent #e2452b, a ruler running under all slides). Use for money maths.
  - tb.html: deep green poster (Anton caps, red tape with numbered seals, still-life photos). Use for checklists and buyer protection.
  - tc.html: near-black data story (Space Grotesk, orange #ff6a1a data accents, cinematic photos, source ticker). Use for data and reports.
- New looks are welcome when they fit the topic, but keep the TrueYards header so the feed stays recognisable. Rishi's taste: premium, simple, quiet, typographic, real depth and layering; he dislikes cheap template looks, clutter, clipped letters and "AI slop". Mixed case and thin weights are liked; he disliked a serif italic accent (Fraunces) and preferred Jost italic for small accent lines.
- Imagery: only images you make (charts, diagrams, typographic art) or AI images already in engine/img. Do not download photos of people or copyrighted images. Do not use photos of public figures.

## The daily run
1. Read this file and log.md. Check what was posted recently so topics and looks rotate.
2. If queue/ has a folder, publish the oldest one (skip to step 6). Otherwise make a new post (steps 3 to 5).
3. Pick the topic: today's news first (RBI, budget, a fresh report), else the next pillar in rotation. Research with web search; gather every figure with its source and date.
4. Design: write an HTML page that is one continuous canvas, N x 1080 px wide and 1350 px tall (N = 7 to 10), elements with class "t" for text. Render with `node engine/multi.cjs <file.html> N 2`, slice with `python3 engine/slice.py <file.png> N <name> <outdir>` (writes <name>-slide-K.jpg at 2160 x 2700 and a contact sheet <file>-sheet.jpg). Look at the contact sheet and at least two slides at full size. Fix clipped text, overlaps, empty areas and edge issues (multi.cjs prints "EDGE" lines for text too close to a slide edge). Downscale slides to 1080 x 1350 JPEG.
5. Write caption.txt: first line restates the hook with keywords; short body; a send prompt naming who to send it to; the source line; the disclaimer; at most 5 hashtags. Under 2,200 characters.
6. Move/copy the slides to posts/<YYYY-MM-DD>-<slug>/slide-1.jpg ... and caption.txt. Commit and push to main. Raw URLs: https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/posts/<folder>/slide-K.jpg. Wait about 30 seconds after pushing.
7. Publish with Windsor.ai: connector "instagram", action "create_carousel_post", account "17841429830946947", params {image_urls: [...in order...], caption}. If it fails because an image cannot be fetched, wait a minute and retry once.
8. Append a row to log.md and push.
9. Final message for Rishi (pushed to his phone): first line bold "TrueYards post live, <date>", then the title, one line on why this topic, and a reminder to add a music track from his phone (carousels with music reach more; the API cannot attach music). No em dashes.

## Limits
- Windsor free plan: only this Instagram account is connected; the Facebook Page is not. Turn on Instagram's "share to Facebook" in the app for cross-posting.
- Max 10 images per carousel through the API.
- If Windsor reports the account disconnected or write actions disabled, stop and tell Rishi in one line.
