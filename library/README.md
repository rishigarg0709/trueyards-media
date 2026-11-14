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
