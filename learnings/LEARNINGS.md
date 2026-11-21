# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-21-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:14 UTC 21 Nov; 20 TrueYards posts returned on Instagram, the Forteasia reel excluded; the Start here carousel of 20 Nov is not yet in the Instagram media list). Noida, Steel rods and Delhi sit in the TrueYards Follow ad set: their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level (Facebook returns a per-reel follower count).
- Followers: IG 415 (+3 in 24 h), FB page 6 (+0), YouTube 2 subscribers (+1, the first new one; channel 1,970 views), Threads 11 (+0), X not returned. Progress to 100,000: 0.42%.
- Follows per 1,000 reach (account): 20 Nov had 9,026 IG reach (about 8,000 paid) and +3 followers, about 0.3 per 1,000. Growth ad 20 Nov: INR 176.77, 318 profile visits, about +2 followers beyond the organic baseline. Since launch: about 149 visits per new follower. Funnel stage: journey (visitors do not follow). Alternative: profile-visit optimisation finds casual tappers.
- Four trials in a row stalled at the first test (NEW, early sign): Jaipur 134 reach, skip 64.0%; Mumbai rent 95, 81.7%; SC stalled loans 115, 80.7%; Kerala empty houses 104, 79.0%. SC and Kerala followed the L13 fix (contradiction line on a bright photoreal object, D1 brightness passed: YAVG 102 and 151) and still lost 4 in 5 viewers in 3 s. So the opening frame is not the only cause. Diagnosis: distribution stage; trials now get a first test of about 100 non-followers, and Instagram stops when skip is high. Alternatives: (a) the openings still read as text cards over images, not as a moving scene (Kerala opened on a light card with ink text; SC on a red label bar); (b) news and regional topics (Kerala, SC order) do not stop a national cold audience. Next test: one reel that opens on full-frame motion with the line spoken, no text card in the first 1.5 s.
- Best reel (still): Steel rods trial (18 Nov midday, 70 h): reach 1,662, skip 34.9%, hold 42.5%, 2 sends (1.2 per 1,000), 2 saves. Top on Facebook (780 plays) and YouTube (674 views, 77% average view). Not a D18 strong trial (hold under 45%, sends under 2 per 1,000); already on the grid.
- Trials so far (D18, trials only, last 10): Steel rods 1,662 reach, skip 34.9%; Japan 407, 47.5%; Jaipur 134, 64.0%; SC 115, 80.7%; Kerala 104, 79.0%; Mumbai 95, 81.7%. Median reach 125, median skip 71.5%. No trial meets the share-to-everyone bar.
- Sends remain the bottleneck: 4 sends on Instagram across all reels in 7 days (Delhi 2, Steel rods 2), 0 comments.
- Carousels reach 7 to 16 accounts on Instagram; Threads is their channel.

### Hook tournament standings (IG reels, organic; ranked by skip because follows per post are not returned; early sign, no arm has 8 posts)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods trial) | 1 | 1,662 | 34.9% | 42.5% | 1.2 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC news) | 6 | 3,844 | 53.5% | 27.5% | 0.5 |
| 10 Visual shock (Jakarta) | 1 | 188 | 55.3% | 16.4% | 0 |
| 14 Story cold open (Jaipur trial) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan; Mumbai rent trial) | 2 | 147 | 81.9% | 16.5% | 0 |
| Unlogged (15 Nov reel) | 1 | 151 | 71.7% | n/a | 0 |
Contradiction fell from 45.4% to 53.5% median skip after Kerala (79.0%) and SC (80.7%): the line alone does not carry a trial. Archetype 24 leads on 1 reel.

### Story types (early sign)
- Everyday India (something every viewer has seen on their own street) is still the best story type (Steel rods, 1 post: 1,662 reach). Famous national places and real cases next (Delhi 1,569, Noida 1,340).
- Regional India (Kerala, Jaipur) and news (SC order) did not travel on Instagram trials (104 to 134 reach), while national India stories did. India vs global is now less clear: global Japan 407 and Burj 309 beat the last four India trials.
- Money maths (Mumbai rent, home loan) is the weakest on IG.

### Looks and voices (early sign, 1 to 3 reels each)
| Look | Reels | Reach | Skip | Hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods trial) | 1 | 1,662 | 34.9% | 42.5% |
| A Newsroom Red (Delhi, Noida, SC trial) | 3 | 3,024 | 43.9% | 34.0% |
| F Tokyo Neutral (Japan trial) | 1 | 407 | 47.5% | 31.1% |
| E Blueprint line art (Burj) | 1 | 309 | 59.4% | 23.8% |
| B Emerald Doc (Jaipur trial) | 1 | 134 | 64.0% | 16.5% |
| T TrueYards Brand (Jakarta, Mumbai rent, Kerala) | 3 | 387 | 79.0% | 11.8% |
Look T test (D2, 18 to 25 Nov): 3 of 6 look T reels in, all three the weakest of their slot (median skip 79.0% against 47.5% for the other looks). Still confounded with the trial slump (Kerala and Mumbai were trials in the 19 to 20 Nov slump), so not proven. On Facebook look T does fine (Jakarta 219, Kerala 217, Mumbai 201 plays) and Kerala is the top recent post on Threads (66 views).
Voices: Tara (Noida, Steel rods, Mumbai rent) median skip 43.8%; Jessa (Delhi, Japan, Jakarta, SC) 51.4%; George (Burj, Jaipur, Kerala) 64.0%. Confounded with topic.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 735 views, Steel rods 674 (77% average view), Jakarta 218 (88% average view), Mumbai rent 138, Japan 91, Jaipur 89, Kerala 66 (1 day), Delhi 52, SC 17 (1 day), Burj 5. First new subscriber (2). YouTube rewards India real-case and everyday-India stories with a plain title. Rule for reel runs: YouTube title = plain event plus stakes, no puzzle wording. Judge YouTube by subscribers and site visits (D30).
- Facebook: Steel rods 780 plays, Burj 231, Jakarta 219, Kerala 217, Jaipur 204, Mumbai 201, SC 74 (still climbing). Every reel gets about 200 plays whatever its IG result; average watch 1.2 to 5.7 s; Jaipur gave the only per-post follow (1 per 204 plays). Facebook is a reach floor, not engagement.
- Threads: stamp duty carousel 175 views, Kerala reel 66 (p93, 1 day; best Threads reel so far), the SC news text post 50 (p87), reels otherwise 1 to 17. Text-first money facts, news and regional mysteries with a number win. Rule for carousel and reel runs: the Threads text leads with the number and the place in the first line ("Kerala has about 12 lakh empty houses").
- X: 0 to 8 views per post, no engagement. Not a growth channel; text-only cross-posts.
- Underperformed on IG but top 20% elsewhere: Kerala (IG 104, Threads 66 p93, FB 217 p80), Mumbai rent (IG 95, FB 201, Threads 17 p80), Jakarta (IG 188, FB 219 p87, YT 218 p80), Burj (IG 309, FB 231 p93), stamp duty carousel (IG 13, Threads 175 p100). Reverse: Delhi (IG 1,569, YT 52, Threads 11).

## Do more
- Everyday India things people see on their own street but never question (Steel rods: best reel on every platform). Mumbai's black-stained towers, Shani Shingnapur and aangan courtyards are next.
- Open on full-frame motion of the object with the line spoken over it, not a text card over a still, in the first 1.5 s (Kerala and SC opened on text bars and lost 79 to 81% even with a good line; Steel rods opened on bright real rooftops).
- National, not regional, stories for Instagram trials (Delhi, Noida, Steel rods 1,340 to 1,662 vs Kerala and Jaipur 104 to 134); regional stories still go out but lean on Threads and Facebook.
- Follow conversion: paid visitors still do not follow (about 149 visits per follower). Pin the Start here carousel and keep the first 3 grid tiles the strongest reels.
- Threads text: number and place in line one (Kerala 66, stamp duty 175 vs price myth 13).

## Do less
- Number slam as the first frame of a reel (home loan 82.1%, Mumbai rent 81.7%).
- Text cards or label bars as the first frame, even with a contradiction line (Kerala 79.0%, SC 80.7%).
- Year-led story cold opens (Jaipur 1876: 64%).
- Dark or line-art openings (Burj Blueprint 59.4%). D1 brightness rule stands.
- Look T on reels until it wins once (3 of 3 weakest): D2 still runs to 25 Nov, so keep one look T reel a day but pair it with archetype 24 and a full-frame motion opening so the look is the only change.

## Running experiments
- Hook tournament (X1): standings above; next review 2026-11-23. Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels.
- Trial first (D18): trials compared only with trials (6 trials, median reach 125, skip 71.5%). The last four trials stalled at about 100 reach. If the next 4 trials also stall under 200 reach, the trial route itself is the question for Rishi (proposal only; D18 is his rule).
- Opening frame (new, from 22 Nov): full-frame motion with spoken line vs text card opening. Metric: skip at 24 h, trials only. Min sample 4 reels each side.
- Look T (X3, D2, 18 to 25 Nov): 3 of 6 reels in, median skip 79.0% vs 47.5%. Review 2026-11-25.
- Geography: national India vs regional India vs global on IG trials. National 1,340 to 1,662; global 309 to 407; regional 104 to 134. Early sign.
- Reel length: all reels 47 to 57 s; still need one 35 to 45 s reel.
- Growth ads (X4): TrueYards Follow, INR 200/day, 3 reels in one ad set (D28). Since 18 Nov 16:45: INR 525, about 1,044 profile visits (INR 0.50 each), +7 followers gross (about +4 net), about INR 75 gross and INR 131 net per new follower. 20 Nov: INR 176.77, 318 visits, about +2 net. Meta gives Noida almost all spend (Steel rods INR 0.03 and Delhi INR 0.10 on 20 Nov). Formal check against INR 12 per follower in the 22 Nov run.
- Posting slot: midday vs evening. Midday median 407 (Delhi 1,569, Steel rods 1,662, Japan 407, Jaipur 134, SC 115) vs evening 188 (Noida 1,340, Burj 309, Jakarta 188, Kerala 104, Mumbai 95). Confounded.
- Remixes queued (14-day rule): Delhi (Lutyens cold open, Paris), Noida (minute-by-minute retelling, Maradu), Steel rods (black water tanks, building one floor at a time, from 2 Dec).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
- 2026-11-20: the 19 Nov trials failed at the hook (Jaipur cold open skip 64%, 134 reach; Mumbai rent number slam skip 81.7%, 94 reach); number slam openings now 2 of 2 failures; look T 2 of 2 weakest; growth ad spent INR 200 for 446 profile visits and 0 follows (IG flat at 412), Delhi added as a third ad; every reel gets about 200 Facebook plays regardless of IG.
- 2026-11-21: four trials in a row stalled at about 100 reach (Jaipur, Mumbai, SC, Kerala; skip 64 to 82%), including two that used the L13 fix, so text-card openings and regional topics are the new suspects; contradiction median skip fell to 53.5%; look T 3 of 3 weakest; IG 415 (+3), first new YouTube subscriber; growth ad INR 176.77 for 318 visits and about +2 net followers (about INR 131 net per follower since launch); Kerala is the best recent Threads post (66).
