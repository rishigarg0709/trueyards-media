# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-22-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:20 UTC 22 Nov; 22 TrueYards posts on Instagram, Forteasia reel excluded; the 21 Nov music-only stilt reel is not posted yet, N47). Steel rods, Delhi, Noida, Burj and Jakarta have had growth ads: their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level (Facebook per-reel follower counts are all 0).
- Followers: IG 420 (+5 in 24 h, best day since launch), FB page 6 (+0), YouTube 4 subscribers (+2), Threads 11 (+0), X not returned. Progress to 100,000: 0.42%.
- Follows per 1,000 reach (account): 21 Nov IG reach 4,754 (paid and organic) for +5 followers, about 1.1 per 1,000 (20 Nov about 0.3). Growth ads in the last 24 h: INR 110.63, about +4 net followers, about INR 28 per net follower (was about INR 88 on 20 Nov). Funnel stage: still journey (about 96 profile visits per new follower since launch), but improving since the spread across reels began.
- Opening test (X14, Signal): the two trials that opened on full-frame motion with the line spoken kept far more viewers than the four text-card trials. Hong Kong tiny homes (21 h) skip 48.5%, 125 reach; Aangan courtyard (15 h) skip 48.9%, 224 reach, against Jaipur 64.0%, Mumbai rent 81.7%, SC 81.0%, Kerala 79.0% (median 80.0%). That is about 51% of viewers past 3 s against about 20%, 2.5 times. Aangan is look T and matched Hong Kong in look F, so the opening, not the look, was the main cause of the 19 to 20 Nov slump. Reach is still low (125 to 224) because neither reel has sends yet.
- Best reel (still): Steel rods trial (18 Nov midday, 94 h): reach 1,666, skip 34.9%, hold 42.4%, 3 sends (1.8 per 1,000), 2 saves; top on Facebook (780 plays) and YouTube (676 views). Best of the last 2 days: Aangan (skip 48.9%, 224 reach in 15 h, 2 saves, 3 likes).
- Trials (D18, trials only, last 8): Steel rods 1,666 / 34.9%; Japan 408 / 47.6%; Aangan 224 / 48.9%; Jaipur 134 / 64.0%; Hong Kong 125 / 48.5%; SC 117 / 81.0%; Kerala 104 / 79.0%; Mumbai 95 / 81.7%. Median reach 130, median skip 56.5%. No trial meets the share-to-everyone bar (none has 2 sends or follows per 1,000 with hold 45%+).
- Sends remain the bottleneck: 0 sends on Instagram from the 6 newest reels; 0 comments. Hold is the next gap: the motion-open trials hold only 21 to 23% (viewers stay past 3 s, then leave by mid-reel).
- Carousels reach 9 to 17 accounts on Instagram (paused to 28 Nov by D41); Threads is their channel.

### Hook tournament standings (IG reels, organic; ranked by skip because per-post follows are not returned)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods trial) | 1 | 1,666 | 34.9% | 42.4% | 1.8 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC, Hong Kong, Aangan) | 8 | 4,201 | 48.7% | 23.4% | 0.5 |
| 10 Visual shock (Jakarta) | 1 | 190 | 55.0% | 16.7% | 0 |
| 14 Story cold open (Jaipur trial) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan; Mumbai rent trial) | 2 | 147 | 81.9% | 16.5% | 0 |
| Unlogged (15 Nov reel) | 1 | 152 | 71.7% | n/a | 0 |
Contradiction is the first arm with 8 posts and 3,000+ reach: median skip 48.7% (it recovered from 53.5% on the two motion-open reels). Its skip splits by opening: motion or real-event openings 43.7 to 48.9% (6 reels), text-card openings 79 to 81% (2 reels). Archetype 24 still leads on 1 reel.

### Story types (early sign)
- Everyday India (Steel rods 1,666) and famous national places or cases (Delhi 1,569, Noida 1,344) still lead on Instagram.
- Engineering marvel with an India twist (Aangan) is the best new type: skip 48.9%, top on X and strong on YouTube (315 views in a day).
- Global comparison (Hong Kong) holds viewers on IG (48.5%) and is the top YouTube start (341 views in a day).
- Regional India and news (Kerala, SC) lose on IG but win on Threads and Facebook. Money maths (Mumbai rent, home loan) is the weakest on IG.

### Looks and voices (early sign, 1 to 4 reels each)
| Look | Reels | Reach | Skip | Hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods trial) | 1 | 1,666 | 34.9% | 42.4% |
| A Newsroom Red (Delhi, Noida, SC trial) | 3 | 3,030 | 43.9% | 34.0% |
| F Tokyo Neutral (Japan, Hong Kong trials) | 2 | 533 | 48.1% | 26.2% |
| E Blueprint line art (Burj) | 1 | 310 | 59.5% | 23.7% |
| B Emerald Doc (Jaipur trial) | 1 | 134 | 64.0% | 16.5% |
| T TrueYards Brand (Jakarta, Mumbai rent, Kerala, Aangan) | 4 | 613 | 67.0% | 14.3% |
Look T test (D2, 18 to 25 Nov): 4 of 6 in. Aangan (look T with a motion opening) skip 48.9% matched Hong Kong in look F (48.5%) the same day, so the earlier look T losses were the text-card openings, not the colours. Look T still has the lowest hold. Call at 25 Nov.
Voices: Tara (Noida, Steel rods, Mumbai rent, Aangan) median skip 46.3%; Jessa (Delhi, Japan, Jakarta, SC, Hong Kong) 48.5%; George (Burj, Jaipur, Kerala) 64.0%. Confounded with topic and opening.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 735, Steel rods 676, Hong Kong 341 (1 day, p83), Aangan 315 (1 day, 13 engagements, the most of any Short in its first day), Jakarta 219, Mumbai rent 143, Kerala 112, Japan 94, Jaipur 94, Delhi 52, SC 20, Burj 5. Subscribers 2 to 4. YouTube rewards everyday-India, engineering and global-comparison stories with a plain title. Rule for reel runs: YouTube title = plain question or event plus the stakes, no puzzle wording. Judge YouTube by subscribers and site visits (D30).
- Facebook: Steel rods 780 plays, Kerala 249, Burj 232, Jakarta 219, Jaipur 206, Mumbai 201, SC 76; the 21 Nov reels are still under 1 day (15 and 4). Every reel gets about 200 plays within 2 days whatever its IG result; average watch 1.2 to 5.7 s. Facebook is a reach floor, not engagement.
- Threads: stamp duty carousel 175 views, Kerala reel 104 (p94), SC news text post 50 (p88); other reels 1 to 17. Text-first money facts, news and regional mysteries with a number win. Rule for reel and carousel runs: the Threads text leads with the number and the place in the first line.
- X: Aangan 10 and Hong Kong 9 views are the best X posts ever; still no follows. Not a growth channel; text-only cross-posts.
- Underperformed on IG but top 20% elsewhere: Hong Kong (IG 125, YT 341 p83, X p94), Kerala (IG 104, FB 249 p94, Threads 104 p94), Mumbai rent (IG 95, Threads p82), Jakarta (IG 190, FB 219 p82), Burj (IG 310, FB 232 p88), stamp duty carousel (IG 14, Threads 175 p100). Reverse: Delhi (IG 1,569, YT 52, Threads 11).

## Do more
- Open every reel on full-frame motion of the object with the line spoken from 0 s, no text before 1.5 s (Hong Kong 48.5% and Aangan 48.9% skip vs 64 to 82% for the four text-card trials). This is now the default for 80% of reels (D41, D42 act-at-Signal).
- Everyday India things people see on their own street but never question (Steel rods: best reel on every platform). Next: balcony grills, refuge floors, not-for-sale walls, shop below the house.
- Engineering with an India twist and global comparisons for YouTube (Aangan 315, Hong Kong 341 in the first day).
- Fix hold after 3 s: the motion-open trials hold 21 to 23%; put the "tell a friend" fact by 40% of the reel and cut each beat to under 4 s.
- Threads text: number and place in line one (Kerala 104, stamp duty 175).

## Do less
- Text cards or label bars as the first frame (Kerala 79.0%, SC 81.0%, Mumbai 81.7%).
- Number slam as the first frame (home loan 82.1%, Mumbai rent 81.7%).
- Year-led story cold opens (Jaipur 1876: 64%).
- Dark or line-art openings (Burj Blueprint 59.5%).
- Judging look T on reels that also had a text-card opening: compare looks only with the opening fixed.

## Running experiments
- Hook tournament (X1): contradiction 8 reels, median skip 48.7%, hold 23.4%; archetype 24 1 reel 34.9%. Next review 2026-11-23. Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels.
- Opening (X14): full-frame motion with spoken line vs text-card opening, skip at 24 h, trials only. 2 motion reels (48.5%, 48.9%) vs 4 text-card reels (median 80.0%). Signal; min sample 4 each side. Final read when 2 more motion-open trials are 24 h old.
- Trial first (D18): 8 trials, median reach 130, skip 56.5%. If the next 2 motion-open trials also stay under 300 reach at 72 h, the question is distribution (sends), not the hook.
- Look T (X3, D2, 18 to 25 Nov): 4 of 6 reels in, median skip 67.0% vs 48.1% for the other looks, but the only look T reel with a motion opening (Aangan) tied look F. Review 2026-11-25.
- Geography: national India 1,340 to 1,666 IG reach; global 125 to 408; regional 104 to 134. Early sign. Hong Kong and Aangan say global and engineering topics do well on YouTube.
- Reel length: all reels 46 to 57 s; still need one 35 to 45 s reel to test hold.
- Growth ads (X4): since 18 Nov 16:45 INR 635.80, about 1,150 profile visits, +12 gross and about +8 net followers: INR 53 gross, about INR 79 net per follower. Last 24 h (spread across Burj and Jakarta, D40): INR 110.63, about +4 net, about INR 28 net. The INR 12 check failed; proposal with Rishi (N50).
- Posting slot: midday median reach 408 (Delhi, Steel rods, Japan, Jaipur, SC, Hong Kong) vs evening 224 (Noida, Burj, Jakarta, Mumbai, Kerala, Aangan). Confounded.
- Remixes queued (14-day rule): Delhi (Lutyens cold open, Paris), Noida (minute-by-minute retelling, Maradu), Steel rods (black water tanks, one floor at a time, from 2 Dec), Kerala (akiya, Gulf mansions, from 4 Dec).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
- 2026-11-20: the 19 Nov trials failed at the hook (Jaipur cold open skip 64%, 134 reach; Mumbai rent number slam skip 81.7%, 94 reach); number slam openings now 2 of 2 failures; look T 2 of 2 weakest; growth ad spent INR 200 for 446 profile visits and 0 follows (IG flat at 412), Delhi added as a third ad; every reel gets about 200 Facebook plays regardless of IG.
- 2026-11-21: four trials in a row stalled at about 100 reach (Jaipur, Mumbai, SC, Kerala; skip 64 to 82%), including two that used the L13 fix, so text-card openings and regional topics are the new suspects; contradiction median skip fell to 53.5%; look T 3 of 3 weakest; IG 415 (+3), first new YouTube subscriber; growth ad INR 176.77 for 318 visits and about +2 net followers (about INR 131 net per follower since launch); Kerala is the best recent Threads post (66).
- 2026-11-22: the two full-frame motion openings (Hong Kong, Aangan trials) kept 2.5 times more viewers past 3 s than the four text-card trials (skip 48.5 and 48.9% vs median 80.0%), and Aangan in look T matched look F, so openings, not looks, caused the slump; contradiction reaches 8 reels (median skip 48.7%); IG 420 (+5, best day), YouTube 4 subscribers (+2), Hong Kong and Aangan are the best first-day Shorts (341 and 315 views); growth ads INR 110.63 for about +4 net followers in 24 h (about INR 28 each), still above the INR 12 line, proposal to Rishi (N50).
