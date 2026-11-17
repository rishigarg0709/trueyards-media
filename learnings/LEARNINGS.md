# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-17-media.csv (pull 05:09 UTC 17 Nov, 9 TrueYards posts plus 1 excluded Forteasia reel). No post is final yet at 72 h; nothing has been boosted (campaign paused, 0 ads), so all numbers are organic. Followers 408 (404 at 10:37 UTC 16 Nov, so +4). Account reach on 16 Nov: 2,871 (previous best day 142); 7-day reach 3,099, of which only 14 from followers, so reels are reaching non-followers as designed.
- The 16 Nov reels are a step change. Delhi skyscrapers (20 h): reach 1,545, skip 43.9%, hold 34% (19.6 s of 57 s), 2 sends (0.13%), 1 save, likes 1.0%, views/reach 1.12. Noida twin towers (15 h): reach 1,301, skip 43.8%, hold 38% (20.6 s of 54.6 s), 0 sends, 4 saves (0.31%, our best), likes 0.9%, views/reach 1.16. Older reels: untitled 15 Nov reel 142 reach, skip 71.8%; home loan reel (14 Nov, 24 s) 42 reach, skip 87%, hold 24%.
- Both 16 Nov reels pass the reach half of the breakout rule (more than 10x the median of our other reels) but fail the sends half (under 1%). Funnel diagnosis: distribution solved for now (hook plus first frame), message stage is the bottleneck: viewers watch but do not send or like. Alternative explanation: a brand-new account with 408 followers gets little social proof, so likes and sends lag regardless of payoff.
- Likes per reach on the big reels (0.9 to 1.0%) are under the 2% weak line. Hold 34 to 38% is just under the 40% good line for 55 s reels.
- Carousels reach only 6 or 7 accounts each (all four of 14 to 16 Nov), with 3 likes each and 0 saves. They are not being distributed beyond a handful of followers; judge them on saves and follows only once reach is meaningful.
- Skip rate at the first 16 Nov pull was 25% on Delhi; it settled to 43.9% as reach widened. Expect skip to rise as a reel reaches colder audiences; compare at equal ages.
- Follows and profile visits per reel are still not returned by the API; use daily account follower change.

### Hook tournament standings (reels, organic, early sign: no arm has 8 posts)
| Archetype | Posts | Reach | Median skip | Median hold | Sends/reach |
|---|---|---|---|---|---|
| 1 Contradiction (Delhi forbidden/contradiction; Noida contradiction + stakes) | 2 | 2,846 | 43.9% | 36% | 0.07% |
| 2 Number slam (home loan reel, archetype inferred, 24 s) | 1 | 42 | 87% | 24% | 0% |
| Unlogged (untitled 15 Nov reel) | 1 | 142 | 71.8% | n/a | 0% |
| Myth bust, stakes, story cold open, visual shock, versus, why does X look like this | 0 | | | | |
Leader so far: contradiction (early sign). Next: test the other six archetypes at the same 45 to 55 s motion-graphic format before calling anything.

### Story types (early sign)
- Familiar Indian anchor plus a puzzle (Delhi: "why no skyscrapers") and a real case with a dramatic event (Noida: towers demolished) both won reach. Money maths (home loan cost) lost badly, though it was also a 24 s reel with old hook rules, so format and hook are confounded.
- Saves came from the story with a buyer lesson (Noida: 4 saves); sends came from the city puzzle (Delhi: 2 sends).

## Do more
- Frame-0 built event plus on-screen number plus beat drop on the hook word (Delhi, Noida: skip 44% vs 72 to 87% on older reels). Early sign across 2 reels; confirm over 8.
- Story-driven topics with a famous Indian place or case (Delhi, Noida: 1,545 and 1,301 reach vs 42 to 142 for others).
- 45 to 57 s length is holding 20 s of watch; keep mini-reveals every 5 to 8 s and work on the second half to push hold past 40%.
- Make the payoff sendable: end with a line a viewer would forward to a specific person (an NCR flat buyer, a Delhi friend). Sends are the gap (0.13% and 0%).
- Add a buyer-lesson beat (what to check) to stories; Noida's 4 saves suggest people keep practical takeaways.

## Do less
- Rishi disliked and deleted the 2026-11-16 carousel "Your EMI didn't change. Your loan did." (dark green, text-heavy, hourglass and house model, RBI repo explainer). Why (Rishi): unlike the first carousels it lacked the big Gemini 3D models and still-life objects on nearly every slide, crossing slide edges; the middle slides were text-only. See PLAYBOOK.md visual richness rules.
- Short money-maths reels without a story (home loan reel: 24 s, skip 87%, reach 42). One post, so early sign only.
- Posting a reel without a log.md entry (the 15 Nov reel DfxHQD6vKff has no caption and no log line, so it cannot be scored against hooks or story types). Every post needs its log line.

## Running experiments
- Hook tournament (weeks 1 to 4): number slam, contradiction, stakes, myth bust, story cold open, visual shock, versus, why does X look like this; tag each in log.md. Standings above; review weekly (next 2026-11-23). Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels.
- Reel length: 35 to 45 s vs 46 to 55 s. Both current winners are 54 to 57 s; need 35 to 45 s reels with the new hook rules to compare.
- Topics: no quotas (Rishi). Story-first across the whole real estate scope; story types tracked above.
- Carousels: slide 2 as a second hook; judge on saves and follows. Blocked by distribution (6 to 7 reach each); try music on carousels if the route allows.
- Accent colour: red vs green vs amber. Both winners used red; no green or amber reels yet.
- Trial twins (daily, midday reel): main hook vs trial hook on the same body, shown to non-followers. No pairs logged yet.
- Posting slot: midday vs evening. Delhi (midday) 1,545 reach in 20 h; Noida (evening) 1,301 in 15 h. Roughly equal per hour; 1 post each.
- Voice: Jessa (Delhi) vs Tara (Noida) roughly tied on skip (43.9 vs 43.8) and hold (34 vs 38%). George untested with new hook rules.
- Delhi remix (top post for sends): Lutyens' Delhi cold open, Paris skyscraper contradiction, Delhi height-rules carousel queued in queue/reel-topics.md.

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
