# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-24-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:14 UTC 24 Nov; 27 TrueYards posts on Instagram, Forteasia reel excluded). Steel rods, Delhi, Noida, Burj, Jakarta and now Bengaluru (from 23 Nov 20:23) have had growth ads: their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level. From 23 Nov reels post to the grid, not as trials (D54).
- Followers: IG 430 (+8 in 24 h, the best day so far), FB page 6 (+0), YouTube 6 subscribers (+2), Threads 12 (+1), X not returned. Progress to 100,000: 0.43%.
- Follows per 1,000 reach (account): 23 Nov IG reach 7,142 (paid and organic) for about +8 followers, about 1.1 per 1,000 (22 Nov about 0.3). Growth ads in the same 24 h: about INR 235 and about 157 paid profile visits (all from the warm spread campaign), so about 1 follower per 20 paid visits against about 1 in 96 before (D54 compares this for a week). Early sign: one day.
- Paid finding (new, D42 lopsided): the three all-India ads made with boost_post (Steel rods, Delhi, Bengaluru) record 0 profile visits: INR 38.07 and 1,192 reach this morning, against 38 visits for INR 40.28 on the two spread ads. boost_post builds the ad without the "Visit Instagram profile" button that follow_setup and follow_spread add (scripts/meta_ops.py), so the all-India campaign buys video views. Raised to Rishi (NeedsRishi) and the SMX chat (LIVE_STATUS).
- Steinway Tower (23 Nov evening, first grid reel under D54, look T, George, scale awe, 51.9 s): 126 reach in 14 h, skip 55.2%, hold 19.5%. Weak on IG so far but 440 YouTube views in its first day (p80, best first day after Aangan) and the best X post of the day (17 views, p95).
- Cost-of-flat carousel (23 Nov, first D54 evergreen carousel): 10 reach, 1 save (10% of reach) on IG; 93 views on Threads (p91). Carousels are judged on profile visitors who follow, not reach.
- Hold: Steinway 51.9 s holds 19.5% against 15.7 to 17.1% for the three 56 to 60 s reels of 22 Nov. Early sign that shorter helps; X18 still has 0 reels at 35 to 45 s.
- Best reel of the last 7 days (per-post follows are not returned, so by reach, skip and hold): Steel rods (18 Nov), reach 1,673, skip 34.9%, hold 42.3%, 3 sends (1.8 per 1,000). Newest strong one: Bengaluru lake, 1,184 reach, skip 49.7%, hold 15.7%, 0 sends; reach has flattened (1,126 to 1,184 in 24 h).
- Trials (D18 ended 23 Nov): last 10 trials median reach 134, median skip 56.8%. None meets the share-to-everyone bar (skip under 35%, hold 45%+, 2 sends or follows per 1,000). Under D54 the trials that worked (Steel rods, Bengaluru, Japan, Aangan) are already listed for Share to everyone in NeedsRishi N57.
- Sends: 0 on Instagram from the 11 newest reels. Comments 0.

### Hook tournament standings (IG reels, organic; ranked by skip because per-post follows are not returned)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods, Shani Shingnapur) | 2 | 1,785 | 44.0% | 29.6% | 1.7 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC, Hong Kong, Aangan, Carpet, Bengaluru) | 10 | 5,615 | 49.9% | 22.3% | 0.4 |
| 10 Visual shock (Jakarta) | 1 | 198 | 54.8% | 16.1% | 0 |
| 23 Scale awe (Steinway, new) | 1 | 126 | 55.2% | 19.5% | 0 |
| 14 Story cold open (Jaipur) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan, Mumbai rent) | 2 | 153 | 82.0% | 15.9% | 0 |
Contradiction (10 reels, past the bar) leads on volume; inside it, a famous place or real case reaches 1,184 to 1,580 (Delhi, Noida, Bengaluru) against 104 to 414 on a generic object or a global city (L17). Archetype 24 leads on skip but has only 2 reels.

### Story types (early sign unless marked)
- Famous Indian place or case with a hidden past or rule, or a thing on every Indian street: Steel rods 1,673, Delhi 1,580, Noida 1,353, Bengaluru 1,184. The only reels over 1,000 reach (L17, Signal).
- Engineering marvels and global comparisons (Aangan, Hong Kong, Steinway) are weak on IG (126 to 252) but lead YouTube (526, 434, 440 views).
- Rules or money maths on a generic object (Carpet 161, Mumbai rent 95, home loan 58) are the weakest on IG; regional India and news (Kerala, SC) lose on IG but win on Threads and Facebook.
- Small-place curiosity without a famous name (Shani 112, Kerala 104, Jaipur 134) does not travel.

### Looks and voices (early sign)
| Look | Reels | Reach | Median skip | Median hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods) | 1 | 1,673 | 34.9% | 42.3% |
| A Newsroom Red (Delhi, Noida, SC) | 3 | 3,050 | 44.0% | 34.1% |
| F Tokyo Neutral (Japan, Hong Kong, Carpet) | 3 | 709 | 49.6% | 21.6% |
| T TrueYards Brand (Jakarta, Mumbai rent, Kerala, Aangan, Bengaluru, Steinway) | 6 | 1,959 | 55.0% | 15.9% |
| B Emerald Doc (Jaipur, Shani) | 2 | 246 | 58.6% | 16.7% |
| E Blueprint line art (Burj) | 1 | 316 | 59.6% | 23.2% |
Look T test (D2, X3, ends 25 Nov): 6 reels, median skip 55.0%. With a motion opening look T (Aangan 50.0%, Bengaluru 49.7%, Steinway 55.2%) sits inside the 49.6 to 60.5% range of other motion-open reels; its 2 big losses were text-card openings. Look is not the cause of wins or losses; the topic and opening are. Final call in tomorrow's run.
Voices (confounded with topic): Tara (Noida, Steel rods, Mumbai rent, Aangan, Bengaluru) median skip 49.7%, 4,557 reach; Jessa (6 reels) 52.2%; George (Burj, Jaipur, Kerala, Shani, Steinway) 59.6%, 792 reach. George now 5 of 5 above 52% skip: early sign, near the bar.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 738, Steel rods 683, Aangan 526 (p87), Steinway 440 (p80, first day), Hong Kong 434, Jakarta 223, Mumbai 143, Shani 125, Kerala 114, Jaipur 99, Japan 91, Delhi 53, SC 21, Bengaluru 11, Burj 5. Subscribers 6 (+2 today). Engineering marvels and global scale stories win on YouTube while the famous-India stories that win IG (Delhi 53, Bengaluru 11) do not. Rule for reel runs: YouTube title is the plain question plus the scale number ("435 m tall, 18 m wide: how does it stand?"), no puzzle wording; judge by subscribers (D30).
- Facebook: Steel rods 781, Kerala 274, Bengaluru 238 (p91), Burj 232, Jakarta 221, Steinway 212 (p77, first day), Jaipur 210, Mumbai 203, SC 77; carousels and most others under 20. Facebook gives about 200 plays to almost any reel with a place name; it is a reach floor, not engagement.
- Threads: stamp duty carousel 175, Kerala 104 (p95), cost-of-flat carousel 93 (p91, first day), SC news text 50, Bengaluru 44; reels 0 to 17. Carousel and checklist text with a rupee number does best on Threads. Rule: Threads text leads with the number and the place in line one; carousels go to Threads as a numbered text list.
- X: Bengaluru 26 (p100), Steinway 17 (p95), Carpet 12, Aangan 11, Shani 11. Still single and low double digits, no follows. Text-only cross-posts are enough.
- Underperformed on IG but top 20% elsewhere: Steinway (IG 126, YT p80, X p95), cost-of-flat carousel (IG 10, Threads p91), Aangan (IG 252, YT p87), Hong Kong (IG 134, YT 434), Kerala (IG 104, FB p95, Threads p95), Shani (IG 112, X p86), stamp duty carousel (IG 20, Threads p100). Reverse: Delhi (IG 1,580, YT 53, Threads 11) and Bengaluru (IG 1,184, YT 11).
- Same everywhere: Steel rods is top on IG, FB and YouTube; Bengaluru top 20% on IG, FB, Threads and X.

## Do more
- Contradiction or "why does X look like this" on a FAMOUS Indian place or a thing on every Indian street, with a hidden past or rule (4 reels at 1,184 to 1,673 reach vs 58 to 414 for every other reel, L17). Name the city in the first line.
- Full-frame motion opening with the line spoken from 0 s: now Proven (X14: 5 motion-open trials at 24 h+, median skip 50.0% vs 80.0% for 4 text-card trials; L18).
- Shorter reels: aim for 40 to 48 s (Steinway 51.9 s holds 19.5% vs 16 to 17% at 56 to 60 s; the 52 to 57 s winners held 34 to 42%). Run X18 at 35 to 45 s on the next reel.
- Tara or Jessa as narrator for India stories (Tara 49.7%, Jessa 52.2% median skip vs George 59.6%).
- For YouTube: engineering and global scale stories (Aangan, Hong Kong, Steinway) get 430 to 530 views; keep one a week for YouTube even though IG reach is low.

## Do less
- Rules or money explainers on a generic object or empty room (Carpet 161, Mumbai rent 95, home loan 58). Put the rule inside a famous place or real case instead.
- Small-place curiosities without a name people know (Shani 112, Kerala 104, Jaipur 134).
- Text cards, label bars or a bare number as the first frame (median skip 80%).
- Reels over 55 s (every one since 19 Nov holds under 23%).
- George as the opening voice on IG reels (5 of 5 above 52% skip, early sign).
- Growth ads made with boost_post until the ad carries the Visit profile button (0 profile visits recorded on INR 38 today).

## Running experiments
- Hook tournament (X1): contradiction 10 reels, median skip 49.9%, hold 22.3%; archetype 24 2 reels 44.0%; scale awe (23) joins with Steinway 55.2%. Next review 2026-11-26. Changes our mind: any archetype beating contradiction by 10 points of median skip over 3 or more reels.
- Opening (X14): DONE, Proven (L18). Default for 80% of reels (D41).
- Look T (X3, D2): 6 reels, median skip 55.0%, ties other motion-open looks. Final call 2026-11-25.
- Follow outro (X15, D49): voiced Shani 16.9% hold, Bengaluru 15.7%; silent Carpet 17.1%, Steinway 19.5%. 2 vs 2. Account follows on reel days: voiced Bengaluru day (22 Nov) +2; silent Steinway day (23 Nov) +8 (with more paid visits). Too early.
- Length (X18): 0 short reels yet; Steinway at 51.9 s is the closest data point (hold 19.5%).
- Grid not trial (D54, from 23 Nov): week-long check of reach per reel against the trial period (last 10 trials median reach 134) and followers per profile visit against about 1 in 96. Day 1: Steinway 126 reach in 14 h; about 1 in 20 paid visits.
- Geography (L2): national India famous place 1,184 to 1,673 IG reach (4 reels); global 126 to 414 (5 reels); small-place India 104 to 161 (4 reels). At the bar on the global side; L17 covers it.
- Growth ads (X4, X16, D55): since 18 Nov 16:45 about INR 1,146 on TrueYards Follow and Follow - spread, about 1,530 profile visits, +22 gross (408 to 430), about +16 net: about INR 52 gross and INR 72 net per follower. Warm spread (X16) judged 25 or 26 Nov against the all-India campaign.
- Posting slot: midday median reach 134 vs evening 252. Confounded with topic.
- Remixes queued (14-day rule): Delhi (Lutyens, Paris), Noida (minute-by-minute, Maradu), Steel rods (black tanks, one floor at a time, from 2 Dec), Kerala (akiya, Gulf mansions, from 4 Dec), Bengaluru (Chennai wetlands, Tehri, lake-bed plot check, from 6 Dec), Steinway (from 7 Dec, YouTube-first).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
- 2026-11-20: the 19 Nov trials failed at the hook (Jaipur cold open skip 64%, 134 reach; Mumbai rent number slam skip 81.7%, 94 reach); number slam openings now 2 of 2 failures; look T 2 of 2 weakest; growth ad spent INR 200 for 446 profile visits and 0 follows (IG flat at 412), Delhi added as a third ad; every reel gets about 200 Facebook plays regardless of IG.
- 2026-11-21: four trials in a row stalled at about 100 reach (Jaipur, Mumbai, SC, Kerala; skip 64 to 82%), including two that used the L13 fix, so text-card openings and regional topics are the new suspects; contradiction median skip fell to 53.5%; look T 3 of 3 weakest; IG 415 (+3), first new YouTube subscriber; growth ad INR 176.77 for 318 visits and about +2 net followers (about INR 131 net per follower since launch); Kerala is the best recent Threads post (66).
- 2026-11-22: the two full-frame motion openings (Hong Kong, Aangan trials) kept 2.5 times more viewers past 3 s than the four text-card trials (skip 48.5 and 48.9% vs median 80.0%), and Aangan in look T matched look F, so openings, not looks, caused the slump; contradiction reaches 8 reels (median skip 48.7%); IG 420 (+5, best day), YouTube 4 subscribers (+2), Hong Kong and Aangan are the best first-day Shorts (341 and 315 views); growth ads INR 110.63 for about +4 net followers in 24 h (about INR 28 each), still above the INR 12 line, proposal to Rishi (N50).
- 2026-11-23: Bengaluru lake trial broke out (1,126 reach in 14.5 h, about 9 times the trial median, top 20% on IG, FB, Threads and X) while 0 sends and hold 16%; motion openings now 5 trials at median skip 50.0% vs 80.0% for text cards; contradiction on a famous place is the winning shape (4 reels over 1,000 reach), rules on a generic object the weakest (Carpet 157); look T ties other looks with a motion opening; hold fell to 16 to 17% on 56 to 60 s reels, so a 35 to 45 s length test (X18) starts; IG 422 (+2), growth ads INR 187 on 22 Nov for about +1 net (warm audience day 1, visits dearer); D40 rotation to Steel rods and Delhi not run (this task may not call follow_spread), Burj and Jakarta kept.
- 2026-11-24: IG 430 (+8, best day; about 1 follower per 20 paid visits vs 1 in 96 before), YouTube 6 (+2), Threads 12 (+1); motion openings Proven (X14, L18); Steinway, the first grid reel under D54, is weak on IG (126 in 14 h, skip 55.2%) but p80 on YouTube and p95 on X, so engineering and scale stories are a YouTube fit; George 5 of 5 above 52% skip; the all-India growth ads made with boost_post record 0 profile visits because they lack the Visit profile button (raised to Rishi); Delhi ad paused, Japan added.
