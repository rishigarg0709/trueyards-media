# Image library

Every TrueYards post uses photo-style imagery. Two sources, both usable with no laptop.

## library/ai (AI-generated, made with Gemini, watermark already cropped)
Label any slide that uses these "AI-generated imagery". Never present them as a real place or project.

| File | What it shows | Suits look |
|---|---|---|
| tower-model-cream.jpg | White architectural model of an apartment tower on cream, soft shadow | ta (cream) |
| key-house-envelopes-cream.jpg | Brass key, small white house model, stack of envelopes on cream | ta |
| a_apt.jpg, a_tower.jpg | Apartment and tower studies on cream (used in carpet area post) | ta |
| contract-pen-calculator-green.jpg | Blank contract, fountain pen, brass calculator on deep green | tb (green) |
| coin-stacks-tower-green.jpg | Rising coin stacks beside a white tower model on deep green | tb |
| b_map.jpg, b_papers.jpg, b_stone.jpg | Map, papers and stone still lifes on green (used in six papers post) | tb |
| city-flyover-dusk.jpg | Aerial of dense Indian high-rises and a lit flyover at dusk | tc (dark) |
| metro-elevated-dusk.jpg | Elevated metro train through a city at dusk, light trails | tc |
| expressway-farmland-aerial.jpg | Aerial of an expressway cloverleaf through green farmland, golden light | tc or ta |
| towers-under-construction-dusk.jpg | Towers under construction with cranes at blue hour | tc |
| empty-apartment-balcony.jpg | Empty sunlit apartment room with balcony doors | ta |
| c_docks.jpg, c_inside.jpg, c_park.jpg | Warehouse docks, interior, logistics park (used in warehousing post) | tc |

Do not reuse the same image within 10 posts (check log.md "images" column).

## library/stock (real photos from Unsplash, fetched on demand)
The cloud shell cannot download from images.unsplash.com, so a GitHub workflow does it:
1. Search with the Unsplash connector (search_photos, orientation landscape or portrait). Pick photos with strong light and a clear subject. No recognisable faces, no public figures, no logos or branded hoardings as the subject.
2. For each pick call download_asset (records the download, returns the file URL). Append `&w=2400` to that URL.
3. Write `fetch/<anything>.txt`, one line per photo: `<short-name> <url>`. Commit and push.
4. Wait about 40 seconds (`gh run list -R rishigarg0709/trueyards-media -L 1` shows the run), then `git pull`. Files appear at library/stock/<short-name>.jpg.
5. Credit photographers in the caption: "Photos: Name, Name / Unsplash".
Fetch 2 or 3 more candidates than needed, look at them at full size, and use only the best.

## library/gen (story-specific model photographs, generated daily, free, no laptop)
Default source for the images that make a post feel made for that day's story. A GitHub workflow calls Cloudflare Workers AI. Free allowance: 10,000 neurons a day, reset 05:30 IST.

Models (set "model" per item):
- `@cf/black-forest-labs/flux-2-klein-4b`: the workhorse. About 300 neurons per 1920 x 1280 image, so roughly 25 a day.
- `@cf/black-forest-labs/flux-2-klein-9b`: best quality, about 1,600 neurons per 1920 x 1280 image. Use for the one hero image (at most 2 a day).
- `@cf/black-forest-labs/flux-1-schnell`: old default, 1024 square, looks like a computer render. Rishi rejected this look (14 Nov). Do not use for finished posts.

Steps:
1. Write `gen/<anything>.json`: a list of `{"name","model","width":1920,"height":1280,"prompt"}`. Max 24 items. Commit and push.
2. Wait about 90 seconds (`gh run list -R rishigarg0709/trueyards-media -L 1`), `git pull`. Files land in library/gen/<name>.jpg; library/gen/_last_run.txt lists results and errors.
3. Two variants per subject on klein-4b (names -a, -b), plus the hero once on klein-9b. Look at all at full size, keep the best, delete the rest.

Prompt recipe (this is what produced launch-level images on 14 Nov; keep the wording):
"Editorial product photograph for a premium finance magazine, shot on a medium format camera with a 90mm lens at f/8, soft daylight from the upper left, soft long shadow falling to the right, true-to-life materials, fine paper texture visible, calm and minimal, no text, no letters, no numbers, no logos, no people, no hands, no studio equipment in frame. <SUBJECT, one sentence, physical materials named: 'a handmade architectural scale model of ... built from white museum board with crisp laser-cut edges', 'plain brass coins, smooth blank discs with no markings', 'a slim brass and glass hourglass'>. <PLACEMENT: 'The model sits in the right third of the frame, the left 55 percent of the frame is empty backdrop'>. Background: seamless warm bone-white paper backdrop and tabletop, colour of unbleached cotton paper, evenly lit, no horizon line, no vignette."
- Say "photograph", never "3D render". Name real materials. Never write "softbox" (it draws one in the frame).
- For dark looks swap the background line for "seamless deep green paper backdrop" or "seamless charcoal backdrop".
- Still fails on anything with writing (dials, documents, notes). No people, landmarks or logos.

Blending (see engine/templates/te.html and the proc() recipe in its git history):
- Crop generously around the subject and its shadow, avoiding any stray objects at the frame edge.
- Flat-field: estimate the backdrop from pixels near the border colour, divide the image by it and multiply by the slide background colour, so the backdrop equals the slide colour. Save as PNG with a feathered alpha mask (about 16% on each edge).
- Place at least one model so it is cut by a slide boundary (half on each slide). Rishi singled this out as the thing he loved.
- Label slides "AI-generated imagery".
- If _last_run.txt shows a quota or auth error, do not retry more than once; fall back to library/ai and Unsplash and say so in the final message.
