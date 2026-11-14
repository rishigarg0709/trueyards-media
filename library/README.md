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

## library/gen (story-specific 3D images, generated daily, free, no laptop)
This is the default source for the images that make a post feel made for that day's story. A GitHub workflow calls Cloudflare Workers AI (FLUX schnell, free daily allowance of roughly 20 to 50 images).
1. Write `gen/<anything>.json`: a list of `{"name": "...", "prompt": "..."}` (no other fields; the model rejects a seed). Max 24 items per file. Commit and push.
2. Wait about 60 to 90 seconds (`gh run list -R rishigarg0709/trueyards-media -L 1`), then `git pull`. Files appear at library/gen/<name>.jpg (1024 x 1024). library/gen/_last_run.txt lists what worked and any error.
3. For every image you need, generate 3 or 4 variants (names ending -a, -b, -c; the same prompt gives a different image each call, and small wording changes give more range). Open each at full size and keep only the best. Delete the rejects before committing the post. If none is good, rewrite the prompt once; if still weak, use library/ai or Unsplash instead.

House prompt style (keep it, so the feed looks like one brand):
"Ultra premium 3D render, studio product photography of <subject>, seamless <warm cream | deep emerald green | near-black charcoal> background, soft diffused light, long soft shadow, minimal editorial still life, large empty space on the <left|right|top> for text, photorealistic architectural model materials, extremely detailed, no text"
- Match the background colour to the look (cream for ta, green for tb, near-black for tc) so the image melts into the slide.
- Subjects that work: architectural scale models, miniature dioramas on a slab (expressway, metro, township, warehouse park), towers arranged like a bar chart, keys, house models, simple objects.
- Subjects that fail: dials, clocks, calculators, documents, currency notes, signboards, anything with numbers or letters (the model writes garbled text). Coin piles come out messy; ask for "three neat stacks" at most. No people, no real landmarks or logos.
- Limits: 1024 px square. Use as an image filling up to about 60% of a slide width, feathered into the background. Never stretch one across a full 2160 px cover; for a full-bleed cover use library/ai or an Unsplash photo.
- Label slides that use them "AI-generated imagery".
- If _last_run.txt shows a quota or auth error, do not retry more than once; fall back to library/ai and Unsplash and mention it in the final message.

Proven examples: tower-model-cream-3d.jpg, expressway-diorama-dark-3d.jpg, city-towers-dark-3d.jpg.
