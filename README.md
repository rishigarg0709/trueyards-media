# trueyards-media

Public images for TrueYards (instagram.com/trueyards.in) posts, plus the engine that makes them.

- `PLAYBOOK.md`: the operating manual for the daily posting run. Read it first.
- `engine/`: HTML templates and render scripts (Playwright). `npm install` inside `engine/` for fonts.
- `queue/`: finished posts waiting to be published, oldest first. Each folder has `slide-N.jpg` and `caption.txt`.
- `posts/<date>-<slug>/`: published posts. Instagram fetches slides from raw.githubusercontent.com URLs here, so never delete or rename a published folder.
- `log.md`: everything published, newest last.
