# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
- First pull (2026-11-16, 7 posts): reels reach 28 to 139, avg watch 6 to 18 s (above the platform average of about 8.5 s); carousels reach 4 to 5; zero shares and zero saves on every post. Retention is fine; sendability is the bottleneck.
- Skip rate (reels_skip_rate, available via API): Delhi skyscrapers reel (2026-11-16, new hook rules: built event in frame 0, number on screen, beat drop on hook word) 25%; older reels 71.5%, 86.4%, 88%. Small-account average is about 65%. Early sign the new hook style works; confirm over 8 reels.
- Follows and profile visits are not returned per reel by the API; use daily account follower change instead. Every post must pass the send test in VIRALITY_PLAYBOOK.md.
- Until there are at least 8 posts per hook archetype, follow the week 1 to 4 hook tournament in VIRALITY_PLAYBOOK.md.

## Do more
- (filled in by the daily run)

## Do less
- (filled in by the daily run)

## Running experiments
- Hook tournament (weeks 1 to 4): number slam, contradiction, stakes, myth bust, story cold open, visual shock, versus, why does X look like this; tag each in log.md.
- Reel length: 35 to 45 s vs 46 to 55 s.
- Topics: no quotas (Rishi). Story-first across the whole real estate scope; track which story types win and lean in from data.
- Carousels: slide 2 as a second hook; judge on saves and follows.
- Accent colour: red vs green vs amber.
- Posting slot: midday (12:23) vs evening (19:07).

## History
- 2026-11-16: file created.
