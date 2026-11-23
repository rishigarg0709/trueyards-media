# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-23-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:14 UTC 23 Nov; 25 TrueYards posts on Instagram, Forteasia reel excluded; the music-only stilt reel is still not posted, N47). Steel rods, Delhi, Noida, Burj and Jakarta have had growth ads: their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level.
- Followers: IG 422 (+2 in 24 h), FB page 6 (+0), YouTube 4 subscribers (+0), Threads 11 (+0), X not returned. Progress to 100,000: 0.42%.
- Follows per 1,000 reach (account): 22 Nov IG reach 7,205 (paid and organic) for +2 followers, about 0.3 per 1,000 (21 Nov about 1.1). Growth ads 22 Nov: INR 187.04, 152 profile visits (INR 1.23 each, up from 0.78), about +1 net follower. The warm audience (X16, day 1) made visits dearer without more follows. Funnel stage: journey (visits do not turn into follows).
- Breakout: Bengaluru bus station was a lake (22 Nov evening trial, look T, Tara, contradiction on a famous place, motion opening): 1,126 reach in 14.5 h, about 9 times the trial median (130), skip 49.4%; also the best X post ever (25 views, p100), Threads 40 (p85) and Facebook 223 (p85) in its first day. But hold 16.0%, 0 sends, 0 saves: it is being shown, not shared.
- Motion openings (X14) now 5 trials: Bengaluru 49.4%, Hong Kong 49.6%, Aangan 50.0%, Shani Shingnapur 52.7%, Carpet area 61.3% (median 50.0%) against 4 text-card trials (median 80.0%). Carpet area (contradiction on an empty room plus a tape line, no famous place) is the weakest motion open and stalled at 157 reach.
- Hold is now the main gap: the three 22 Nov reels are 56 to 60 s long (voiced outro adds about 6 s) and hold 16.0 to 17.1%, against 34 to 42% for the 52 to 57 s winners of 16 to 18 Nov. Viewers stay past 3 s and leave before the middle.
- Best reel overall (still): Steel rods trial (18 Nov, 117 h): reach 1,668, skip 34.9%, hold 42.3%, 3 sends (1.8 per 1,000). Best of the last 7 days by follows per 1,000 reach: not measurable per post; by reach, skip and other platforms: Bengaluru.
- Trials (D18, last 10): Steel rods 1,668 / 34.9%; Bengaluru 1,126 / 49.4% (14 h); Japan 409 / 47.8%; Aangan 252 / 50.0%; Carpet 157 / 61.3%; Hong Kong 134 / 49.6%; Jaipur 134 / 64.0%; SC 117 / 81.0%; Shani 111 / 52.7% (21 h); Kerala 104 / 79.0%. Median reach 146, median skip 51.4%. No trial meets the share-to-everyone bar (none has hold 45%+ with 2 sends or follows per 1,000).
- Sends: 0 on Instagram from the 9 newest reels. Comments 0.
- Carousels: paused to 28 Nov (D41); 12 to 17 reach each on Instagram.

### Hook tournament standings (IG reels, organic; ranked by skip because per-post follows are not returned)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods, Shani Shingnapur) | 2 | 1,779 | 43.8% | 29.7% | 1.7 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC, Hong Kong, Aangan, Carpet, Bengaluru) | 10 | 5,529 | 49.8% | 22.3% | 0.4 |
| 10 Visual shock (Jakarta) | 1 | 192 | 54.7% | 16.5% | 0 |
| 14 Story cold open (Jaipur trial) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan; Mumbai rent trial) | 2 | 149 | 82.3% | 16.2% | 0 |
| Unlogged (15 Nov reel) | 1 | 152 | 71.9% | n/a | 0 |
Contradiction (10 reels, past the bar): on a famous place or real case it reaches 1,126 to 1,571 (Delhi, Noida, Bengaluru); on a generic object or abstract idea 104 to 409. Archetype 24 is 2 reels; Shani (52.7%) pulled its median from 34.9% to 43.8%.

### Story types (early sign)
- Famous Indian place or case with a hidden past or rule: Delhi 1,571, Noida 1,346, Bengaluru 1,126 (14 h). Everyday India object: Steel rods 1,668. These four are the only reels over 1,000 reach.
- History of the land (Bengaluru lakes) is the new best type: top on X and strong on Threads and Facebook too.
- Engineering with an India twist (Aangan) and global comparison (Hong Kong) hold viewers on IG and lead on YouTube (446 and 420 views).
- Rules or money maths explained on a generic object (Carpet area 157, Mumbai rent 95, home loan 54) are the weakest on IG; regional India and news (Kerala, SC) lose on IG but win on Threads and Facebook.
- Real case from a small place (Shani Shingnapur) 111 reach in 21 h: a curious fact without a famous name did not travel.

### Looks and voices (early sign, 1 to 5 reels each)
| Look | Reels | Reach | Median skip | Median hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods) | 1 | 1,668 | 34.9% | 42.3% |
| A Newsroom Red (Delhi, Noida, SC) | 3 | 3,034 | 43.9% | 34.0% |
| F Tokyo Neutral (Japan, Hong Kong, Carpet) | 3 | 700 | 49.6% | 21.6% |
| B Emerald Doc (Jaipur, Shani) | 2 | 245 | 58.4% | 16.8% |
| E Blueprint line art (Burj) | 1 | 313 | 59.6% | 23.4% |
| T TrueYards Brand (Jakarta, Mumbai rent, Kerala, Aangan, Bengaluru) | 5 | 1,769 | 54.7% | 16.0% |
Look T test (D2, X3) has its 5 reels: with a motion opening look T does as well as any look (Aangan 50.0%, Bengaluru 49.4% vs 49.6 to 61.3% for the other motion-open trials), and Bengaluru in look T is the biggest trial since Steel rods. Its losses were the text-card openings. Hold is low for every look since 19 Nov, so it is not a look effect. Final call 25 Nov.
Voices (confounded with topic and opening): Tara (Noida, Steel rods, Mumbai rent, Aangan, Bengaluru) median skip 49.4%; Jessa (Delhi, Japan, Jakarta, SC, Hong Kong, Carpet) 52.2%; George (Burj, Jaipur, Kerala, Shani) 61.8%. Early sign: George has the weakest openings 4 of 4.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 736, Steel rods 679, Aangan 446 (p86), Hong Kong 420 (p79), Jakarta 220, Mumbai rent 143, Shani 116 (first day, p57), Kerala 114, Japan 91, Jaipur 95, Delhi 52, SC 20, Burj 5, Bengaluru 5 (just posted). Subscribers flat at 4 for 2 days. Engineering and global comparison still lead new Shorts. Rule for reel runs: YouTube title is the plain question or event plus the stakes, no puzzle wording. Judge YouTube by subscribers and site visits (D30).
- Facebook: Steel rods 780, Kerala 274, Burj 232, Bengaluru 223 (in a day, p85), Jakarta 221, Jaipur 209, Mumbai 202, SC 77, Aangan 16, Shani 17, Hong Kong 5. Facebook gives about 200 plays to India stories with a place name and very little to the rest; it is a reach floor, not engagement.
- Threads: stamp duty carousel 175, Kerala 104 (p95), SC news text 50, Bengaluru 40 (p85, 2 engagements); others 0 to 17. Text-first facts with a number and a place name win. Rule for reel and carousel runs: the Threads text leads with the number and the place in line one.
- X: Bengaluru 25 views (p100), Carpet area 11, Aangan 10, Hong Kong 9, Shani 9. Rising slowly from single digits; still no follows. Text-only cross-posts are enough.
- Underperformed on IG but top 20% elsewhere: Hong Kong (IG 134, YT 420, X p85), Shani (IG 111, X p85), Kerala (IG 104, FB 274 p95, Threads p95), Mumbai rent (IG 95, Threads p80), Jakarta (IG 192, FB 221 p80), Burj (IG 313, FB 232 p90), Carpet area (IG 157, X 11 p95), stamp duty carousel (IG 15, Threads 175 p100). Reverse: Delhi (IG 1,571, YT 52, Threads 11).
- Same everywhere: Bengaluru is top 20% on IG, FB, Threads and X at once, the first reel since Steel rods to win on four platforms.

## Do more
- Contradiction or "why does X look like this" on a FAMOUS Indian place or a thing on every Indian street, with a hidden past or rule (Steel rods 1,668, Delhi 1,571, Noida 1,346, Bengaluru 1,126 in 14 h vs 104 to 409 for every other reel). Name the city in the first line.
- Keep the full-frame motion opening with the line spoken from 0 s (5 trials, median skip 50.0% vs 80.0% for text cards; D41).
- Fix hold: cut the story to 35 to 45 s (the 56 to 60 s reels of 22 Nov hold 16 to 17%), one beat under 3 s, the tell-a-friend fact by 40%. Test X18 below.
- Look T is fine with a motion opening (Aangan, Bengaluru): keep it for one reel a day through 25 Nov.
- Threads and X text: number and place in line one (Bengaluru is the best post on X and top 15% on Threads).

## Do less
- Rules or money explainers on a generic object or empty room (Carpet area 157 reach, skip 61.3%; Mumbai rent 95; home loan 54). Put the rule inside a famous place or real case instead.
- Small-place curiosities without a name people know (Shani 111 in 21 h, Kerala 104, Jaipur 134).
- Text cards, label bars or a bare number as the first frame (Kerala 79.0%, SC 81.0%, Mumbai 81.7%, home loan 82.8%).
- Reels over 55 s: every reel since 19 Nov is 46 to 60 s and holds under 23%.
- George as the opening voice: 4 of 4 reels above 52% skip (confounded, early sign).

## Running experiments
- Hook tournament (X1): contradiction 10 reels, median skip 49.8%, hold 22.3%; archetype 24 2 reels 43.8%. Famous-place contradiction is the leader inside the arm. Next review 2026-11-26. Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels.
- Opening (X14): motion opening 5 trials (2 at 24 h+), median skip 50.0% vs 80.0% for 4 text-card trials. Becomes Proven when Shani, Carpet and Bengaluru reach 24 h (tomorrow's run); already the default (D41).
- Look T (X3, D2): 5 of 5 reels in; with motion openings it ties or beats the other looks. Final call 2026-11-25.
- Follow outro (X15, D49): voiced Shani (hold 17.1%) and Bengaluru (16.0%) vs silent Carpet (16.8%). Per-post follows are not returned, so it is judged on account follows on reel days and on hold; 2 vs 1, too early.
- Length (X18, new): one reel at 35 to 45 s against the 52 to 60 s default, same opening rules. Metric: hold ratio and skip at 24 h. Min sample 3 short reels.
- Trial first (D18): 10 trials, median reach 146, median skip 51.4%; Bengaluru shows a trial can still break out without sends.
- Geography (L2): national India famous place 1,126 to 1,668 IG reach (4 reels); global 134 to 409 (4 reels); small-place India 104 to 157 (4 reels). Early sign, close to the 5-per-side bar.
- Growth ads (X4, X16): since 18 Nov 16:45 about INR 911 on TrueYards Follow and Follow - spread, about 1,370 profile visits, +14 gross (408 to 422), about +9 net: about INR 65 gross and INR 101 net per follower, about 98 visits per gross follower. 22 Nov (first warm-audience day): INR 187, 152 visits, about +1 net. X16 review 25 Nov.
- Posting slot: midday median reach 134 (Delhi, Steel rods, Japan, Jaipur, SC, Hong Kong, Shani) vs evening 252 (Noida, Burj, Jakarta, Mumbai, Kerala, Aangan, Bengaluru). Confounded with topic.
- Remixes queued (14-day rule): Delhi (Lutyens, Paris), Noida (minute-by-minute, Maradu), Steel rods (black tanks, one floor at a time, from 2 Dec), Kerala (akiya, Gulf mansions, from 4 Dec), Bengaluru (Chennai wetlands, Tehri, lake-bed plot check carousel, from 6 Dec).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
- 2026-11-20: the 19 Nov trials failed at the hook (Jaipur cold open skip 64%, 134 reach; Mumbai rent number slam skip 81.7%, 94 reach); number slam openings now 2 of 2 failures; look T 2 of 2 weakest; growth ad spent INR 200 for 446 profile visits and 0 follows (IG flat at 412), Delhi added as a third ad; every reel gets about 200 Facebook plays regardless of IG.
- 2026-11-21: four trials in a row stalled at about 100 reach (Jaipur, Mumbai, SC, Kerala; skip 64 to 82%), including two that used the L13 fix, so text-card openings and regional topics are the new suspects; contradiction median skip fell to 53.5%; look T 3 of 3 weakest; IG 415 (+3), first new YouTube subscriber; growth ad INR 176.77 for 318 visits and about +2 net followers (about INR 131 net per follower since launch); Kerala is the best recent Threads post (66).
- 2026-11-22: the two full-frame motion openings (Hong Kong, Aangan trials) kept 2.5 times more viewers past 3 s than the four text-card trials (skip 48.5 and 48.9% vs median 80.0%), and Aangan in look T matched look F, so openings, not looks, caused the slump; contradiction reaches 8 reels (median skip 48.7%); IG 420 (+5, best day), YouTube 4 subscribers (+2), Hong Kong and Aangan are the best first-day Shorts (341 and 315 views); growth ads INR 110.63 for about +4 net followers in 24 h (about INR 28 each), still above the INR 12 line, proposal to Rishi (N50).
- 2026-11-23: Bengaluru lake trial broke out (1,126 reach in 14.5 h, about 9 times the trial median, top 20% on IG, FB, Threads and X) while 0 sends and hold 16%; motion openings now 5 trials at median skip 50.0% vs 80.0% for text cards; contradiction on a famous place is the winning shape (4 reels over 1,000 reach), rules on a generic object the weakest (Carpet 157); look T ties other looks with a motion opening; hold fell to 16 to 17% on 56 to 60 s reels, so a 35 to 45 s length test (X18) starts; IG 422 (+2), growth ads INR 187 on 22 Nov for about +1 net (warm audience day 1, visits dearer); D40 rotation to Steel rods and Delhi not run (this task may not call follow_spread), Burj and Jakarta kept.
