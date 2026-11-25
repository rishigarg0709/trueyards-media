# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-25-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:16 UTC 25 Nov; 30 TrueYards posts on Instagram, Forteasia reel excluded). Steel rods, Delhi, Noida, Burj, Jakarta, Bengaluru and Japan have had growth ads (Aangan from 25 Nov): their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level. From 23 Nov reels post to the grid, not as trials (D54).
- Followers: IG 439 (+9 in 24 h, new best day), FB page 7 (+1), YouTube 6 subscribers (+0), Threads 12 (+0), X not returned. Progress to 100,000: 0.44%.
- Follows per 1,000 reach (account): 24 Nov IG reach 18,748 (paid and organic, more than double 23 Nov) for +9, about 0.5 per 1,000 (23 Nov about 1.1). The extra reach was mostly the all-India growth ads; more reach did not bring more follows per person reached.
- NEW, grid reels keep viewers better (D54, Signal, L20): the three reels of 24 Nov, all on the main grid, have the lowest skip rates since Steel rods: Chandigarh Sector 13 38.1% (969 reach in 21 h, reach breakout, 7 times the median), Mumbai no-OC 41.7%, Balcony grill 41.1%. The 4 grid reels since D54 have median skip 41.4% against 53.1% for the last 11 trials. Confounded: all three are famous-place or every-street India topics with motion openings (L17, L18).
- Balcony grill (24 Nov evening, look T, Jessa, hook 24, 51.2 s): 384 reach in 15 h, skip 41.1%, average watch 40.0 s of 51.2 s (hold 78.1%, the best ever, almost 2 times Steel rods 42.2%). 1 send, 1 save. X p88.
- Mumbai flats with no OC (24 Nov 17:13 slot, look A, Tara, contradiction, real case, 44.8 s): 131 reach in 17 h, skip 41.7%, hold 27.4%, 3 sends = 22.9 sends per 1,000 reach, the best send rate of any TrueYards reel (Steel rods 1.8). A real case with a loss people fear gets sent. First X18 short reel (44.8 s).
- Chandigarh Sector 13 (24 Nov midday, look B, George, contradiction on a famous place, 50.4 s): 969 reach in 21 h, skip 38.1%, hold 21.2%, 1 send, 11 likes. First George reel under 52% skip, so the George finding was the topic, not the voice. X 24 views (p96).
- Best reel of the last 7 days (per-post follows are not returned, so by reach, skip, hold and sends): Chandigarh for reach and skip; Mumbai no-OC for sends; Balcony for hold.
- Trials (D18 ended 23 Nov): no trial reel meets the share-to-everyone bar (skip under 35%, hold 45%+, 2 sends or follows per 1,000). The 4 trials that worked stay listed in NeedsRishi N57.
- Carousel: cost-of-flat (23 Nov) 16 reach, 1 save, 1 like; carousels are judged on profile visitors who follow (D54).

### Hook tournament standings (IG reels, organic; ranked by skip because per-post follows are not returned)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods, Shani, Balcony grill) | 3 | 2,175 | 41.1% | 42.2% | 1.8 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC, Hong Kong, Aangan, Carpet, Bengaluru, Chandigarh, Mumbai no-OC) | 12 | 6,743 | 49.7% | 22.2% | 0.9 |
| 23 Scale awe (Steinway) | 1 | 140 | 54.3% | 18.6% | 0 |
| 10 Visual shock (Jakarta) | 1 | 203 | 56.4% | 15.7% | 0 |
| 14 Story cold open (Jaipur) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan, Mumbai rent) | 2 | 154 | 82.1% | 15.8% | 0 |
Archetype 24 now leads contradiction by 8.6 points of skip and almost 2 times the hold over 3 reels (2 of them on the grid or Steel rods). Contradiction is past the bar on volume; inside it, a famous Indian place or real case wins (Chandigarh, Delhi, Noida, Bengaluru, Mumbai no-OC).

### Story types (early sign unless marked)
- Famous Indian place or a thing on every Indian street, with a hidden past or rule: Steel rods 1,679, Delhi 1,586, Noida 1,360, Bengaluru 1,191, Chandigarh 969 in 21 h. Still the only reels near or over 1,000 reach (L17, Signal, now 5 reels).
- Real case with a loss people fear (Mumbai no-OC): the only reel with sends over 2 per 1,000. Early sign, 1 reel.
- Engineering marvels and global comparisons (Aangan, Hong Kong, Steinway) are weak on IG (134 to 252) but lead YouTube (548, 435, 454).
- Rules or money maths on a generic object (Carpet 162, Mumbai rent 95, home loan 59) are the weakest on IG.
- Small-place curiosity without a famous name (Shani 112, Kerala 104, Jaipur 134) does not travel.

### Looks and voices (early sign)
| Look | Reels | Reach | Median skip | Median hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods) | 1 | 1,679 | 35.0% | 42.2% |
| A Newsroom Red (Delhi, Noida, SC, Mumbai no-OC) | 4 | 3,194 | 44.0% | 30.7% |
| F Tokyo Neutral (Japan, Hong Kong, Carpet) | 3 | 714 | 49.6% | 21.6% |
| B Emerald Doc (Jaipur, Shani, Chandigarh) | 3 | 1,215 | 53.1% | 16.9% |
| T TrueYards Brand (Jakarta, Mumbai rent, Kerala, Aangan, Bengaluru, Steinway, Balcony) | 7 | 2,369 | 54.3% | 15.7% |
| E Blueprint line art (Burj) | 1 | 319 | 60.2% | 23.1% |
Look T test (D2, X3) FINAL, 25 Nov: 7 reels, median skip 54.3%, hold 15.7%, 2,369 reach. Look T has the worst and the best (Balcony 41.1% skip, hold 78.1%) depending on opening and topic, and every look has a wide range. Verdict: the look does not decide a reel; topic and opening do. Look T stays allowed but is no longer required daily (D2 ends today). Analytics stops tracking looks as a test.
Voices: Tara 6 reels, median skip 46.8%, 4,708 reach; Jessa 7 reels, 49.6%; George 6 reels, 57.2%, but Chandigarh (George) 38.1% shows the earlier George losses were weak topics. Not a rule.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 743, Steel rods 684, Aangan 548 (p88), Steinway 454 (p82), Hong Kong 435, Jakarta 223, Mumbai rent 143, Shani 127, Kerala 116, Chandigarh 106 (first day), Jaipur 103, Balcony 95 (first day), Japan 91, Delhi 59, SC 21, Bengaluru 13, Burj 5. The Mumbai no-OC reel has no YouTube copy. Subscribers 6 (+0). Engineering marvels and global scale stories win YouTube while the famous-India stories that win IG (Delhi 59, Bengaluru 13, Chandigarh 106) do less. Rule for reel runs: YouTube title is the plain question plus the scale number ("435 m tall, 18 m wide: how does it stand?"), no puzzle wording; judge by subscribers (D30). Every reel, including the 17:13 slot, needs its YouTube copy.
- Facebook: Steel rods 781, Kerala 278 (p96), Bengaluru 239, Burj 232, Jakarta 221, Steinway 216, Jaipur 211, Mumbai rent 203, Chandigarh 91 (first day), SC 77, Balcony 47 (first day), Mumbai no-OC 23. Facebook gives about 200 plays to almost any reel with a place name within 2 to 3 days; a reach floor, not engagement. Page followers 7.
- Threads: stamp duty carousel 175, Kerala 104 (p96), cost-of-flat carousel 104 (p96), SC news text 50, Bengaluru 44; reels 0 to 17 (Mumbai no-OC 14, Chandigarh 11). Rule stays: Threads text leads with the number and the place in line one; carousels go to Threads as a numbered text list.
- X: Bengaluru 26 (p100), Chandigarh 24 (p96), Steinway 17 (p92), Balcony 13 (p88), Carpet 12, Aangan 11, Shani 11, Mumbai no-OC 10. A famous Indian place plus a puzzle in the first line does best on X too. Still no follows; text-only cross-posts are enough.
- Underperformed on IG but top 20% elsewhere: Steinway (IG 140, YT p82, X p92), cost-of-flat carousel (IG 16, Threads p96), Aangan (IG 252, YT p88), Hong Kong (IG 134, YT 435), Kerala (IG 104, FB p96, Threads p96), stamp duty carousel (IG 24, Threads p100). Reverse: Delhi (IG 1,586, YT 59) and Bengaluru (IG 1,191, YT 13).
- Same everywhere: Steel rods top on IG, FB and YouTube; Bengaluru and Chandigarh top 20% on IG and X.

## Do more
- "Why does X look like this" on a thing on every Indian street (Steel rods, Balcony grill): 3 reels, median skip 41.1%, hold 42.2%, the best hook so far. At least 1 reel in 3 should be this shape while it leads.
- Contradiction on a FAMOUS Indian place or real case, city in the first line (Chandigarh 969 reach in 21 h, skip 38.1%; L17, 5 reels near or over 1,000).
- Real cases where buyers lost something (Mumbai no-OC: 22.9 sends per 1,000, best ever). Pairs well with X19 shares.
- Full-frame motion opening with the line spoken from 0 s (Proven, L18).
- 44 to 51 s length: Mumbai no-OC 44.8 s and Balcony 51.2 s held 27% and 78%; the 56 to 60 s reels held 16 to 17%.
- For YouTube: one engineering or global scale story a week (Aangan, Hong Kong, Steinway: 435 to 548 views).

## Do less
- Rules or money explainers on a generic object or empty room (Carpet 162, Mumbai rent 95, home loan 59). Put the rule inside a famous place or real case (Mumbai no-OC shows how).
- Small-place curiosities without a name people know (Shani 112, Kerala 104, Jaipur 134).
- Text cards, label bars or a bare number as the first frame (median skip 80%).
- Reels over 55 s (every one since 19 Nov holds under 23%).
- Global engineering stories as the IG reel of the day (Steinway 140 reach, skip 54.3%): keep them, but as the YouTube-first slot.
- Judging growth ads on cheap profile visits: the all-India ads now buy visits at INR 0.64 but L12 says such visits rarely follow.

## Running experiments
- Hook tournament (X1): archetype 24 3 reels, median skip 41.1%, hold 42.2%; contradiction 12 reels, 49.7%, hold 22.2%. Changes our mind: any archetype beating contradiction by 10 points of median skip over 3 or more reels; archetype 24 is at 8.6 points. Next review 2026-11-26.
- Shares (X19, D56): starts with the 25 Nov midday reel (Flat or plot); judge at 72 h on sends per 1,000 reach, then follows per 1,000 reach, 4 per side. Benchmark: Mumbai no-OC 22.9 sends per 1,000 (control-style reel).
- Follow outro (X15, D49): voiced Shani 16.9%, Bengaluru 15.7%, Chandigarh 21.2%, Balcony 78.1% hold; silent Carpet 17.1%, Steinway 18.6%, Mumbai no-OC 27.4%. 4 vs 3 reels. Account follows on reel days: voiced days +2 (22 Nov) and +9 (24 Nov, mixed with silent Mumbai no-OC); silent day +8 (23 Nov). Too early, outro does not hurt hold.
- Length (X18): 1 short reel (Mumbai no-OC 44.8 s, hold 27.4%) against 56 to 60 s reels at 15.7 to 17.1%. 1 of 3.
- Grid not trial (D54, from 23 Nov): 4 grid reels median skip 41.4% vs 53.1% for the last 11 trials; reach Chandigarh 969 and Balcony 384 in under a day vs trial median about 134. Followers per paid profile visit about 1 in 52 in the last 24 h (target better than 1 in 96). Signal (L20); week-long check ends 30 Nov.
- Look T (X3, D2): DONE 25 Nov, no effect of the look; see Looks.
- Geography (L2, L17): national India famous place 969 to 1,679 IG reach (5 reels); global 134 to 418 (6 reels); small-place India 104 to 162 (4 reels).
- Growth ads (X4, X16, D55): since 18 Nov 16:45 about INR 1,841 on TrueYards Follow and Follow - spread, +31 gross (408 to 439), about +24 net: about INR 59 gross and INR 77 net per follower. Last 24 h about INR 695 for +9 gross: about INR 77 gross, INR 87 net, the worst value day, because the all-India campaign spent about INR 342 on 24 Nov (Meta may overspend a daily budget by up to 75%). Warm spread (X16) is judged in the 26 Nov run, after the all-India ads have one full day with the Visit profile button.
- Posting slot: confounded with topic; Chandigarh (midday) is the best midday reel.
- Remixes queued (14-day rule): Delhi (Lutyens, Paris), Noida (minute-by-minute, Maradu), Steel rods (black tanks, one floor at a time, from 2 Dec), Kerala (akiya, Gulf mansions, from 4 Dec), Bengaluru (Chennai wetlands, Tehri, lake-bed plot check, from 6 Dec), Steinway (from 7 Dec, YouTube-first), Chandigarh (from 8 Dec), Mumbai no-OC (from 8 Dec), Balcony grill (from 8 Dec).

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
- 2026-11-25: the three 24 Nov grid reels kept viewers better than any trial since Steel rods (Chandigarh skip 38.1% and 969 reach in 21 h, Balcony grill hold 78.1%, Mumbai no-OC 22.9 sends per 1,000, the best send rate ever), so grid publishing (D54) plus famous-place topics is the new Signal (L20); archetype 24 leads the hook tournament (3 reels, skip 41.1%); look T test closed with no look effect; George's first good reel (Chandigarh) clears the voice; IG 439 (+9, best day), FB 7, YT 6, Threads 12; growth ads about INR 695 in 24 h for +9 (about INR 87 net each), all-India ads now record visits with the button (281 by 10:45 at INR 0.64); Steel rods ad paused after 6 days, Aangan added.
