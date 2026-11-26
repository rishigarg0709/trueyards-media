# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-26-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:17 UTC 26 Nov; 33 TrueYards posts on Instagram, Forteasia reel excluded). Noida, Steel rods, Delhi, Burj, Jakarta, Bengaluru, Japan and Aangan have had growth ads (Balcony grill from 26 Nov): their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level. Reels post to the grid, not as trials (D54).
- Followers: IG 444 (+5 in 24 h), FB page 7 (+0), YouTube 6 subscribers (+0), Threads 12 (+0), X not returned. Progress to 100,000: 0.44%.
- Follows per 1,000 reach (account): 25 Nov IG reach 5,148 for +5 (about 1.0 per 1,000); 24 Nov 21,263 for +12 by the account series (about 0.6). Paid reach keeps adding reach faster than follows.
- NEW, both 25 Nov grid reels are early duds (under 24 h, playbook dud line is skip 60%): Flat or plot (X19 shares reel 1, hook 16 Versus on a tower lifted off its plot, look F, Tara, 43.6 s) 119 reach in 21.5 h, skip 73.2%, hold 19.9%, 0 sends; Ahmedabad pols (X19 control, contradiction, look T, Jessa, 51.6 s) 108 reach in 14.5 h, skip 83.6%, hold 7.1%, 0 sends. Flat or plot is a rule on a generic object (our weakest IG shape, Do less); pols is a regional heritage topic without an all-India hook, like Shani, Kerala and Jaipur. Early sign: a grid slot does not rescue a weak topic.
- Balcony grill (24 Nov evening, hook 24, look T, Jessa, 51.2 s): 876 reach in 39 h (reach breakout, about 5 times the reel median), skip 38.2%, hold 52.8% (best ever, average 27 s of 51 s), 1 send, 1 save. Best reel of the last 7 days on skip and hold; now a growth ad.
- Chandigarh Sector 13 (24 Nov midday, contradiction on a famous place, George): 1,039 reach in 45 h, skip 38.8%, hold 21.0%, 1 send, 11 likes.
- Mumbai no-OC (24 Nov 17:13): 153 reach, skip 41.1%, 4 sends = 26.1 sends per 1,000 reach, still the best send rate of any TrueYards reel.
- Best post of the last 7 days by follows per 1,000 reach: not measurable per post (Instagram returns no follows for reels); by skip, hold and reach it is Balcony grill (skip 38.2%).
- L20 (grid reels hold better) weakens: 6 grid reels now have median skip 48.4% (38.2, 38.8, 41.1, 55.6, 73.2, 83.6) against 53.1% for the last 11 trials, gap 9%. The topic decides, not the grid.
- Trials (D18 ended 23 Nov): no trial reel meets the share-to-everyone bar (skip under 35%, hold 45%+, 2 sends or follows per 1,000; Steel rods is 35.0% skip and 1.8 sends). The 4 trials that worked stay listed in NeedsRishi N57.
- Carousels: possession-day checks (25 Nov) 8 reach in 17 h, 3 profile visits, 0 follows; cost-of-flat (23 Nov) 18 reach. Carousels reach only followers; judged on profile visitors who follow (D54).

### Hook tournament standings (IG reels at least 24 h old, organic; ranked by skip because per-post follows are not returned)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods, Shani, Balcony grill) | 3 | 2,672 | 38.2% | 42.2% | 1.5 |
| 1 Contradiction (Delhi, Noida, Japan, Burj, Kerala, SC, Hong Kong, Aangan, Carpet, Bengaluru, Chandigarh, Mumbai no-OC) | 12 | 6,858 | 49.8% | 22.3% | 1.2 |
| 23 Scale awe (Steinway) | 1 | 144 | 55.6% | 18.2% | 0 |
| 10 Visual shock (Jakarta) | 1 | 207 | 57.2% | 15.7% | 0 |
| 14 Story cold open (Jaipur) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan, Mumbai rent) | 2 | 158 | 82.7% | 15.5% | 0 |
| 16 Versus (Flat or plot, 21.5 h, not yet counted) | 1 | 119 | 73.2% | 19.9% | 0 |
Archetype 24 now leads contradiction by 11.6 points of median skip and almost 2 times the hold over 3 reels, past the X1 change-our-mind line (10 points over 3 reels). Still below the 8-reel pattern bar, so Hunch (L21); act on it under D42 because it is cheap and reversible. Ahmedabad pols (contradiction, 14.5 h, skip 83.6%) joins the contradiction count tomorrow.

### Story types (early sign unless marked)
- Famous Indian place or a thing on every Indian street, with a hidden past or rule: Steel rods 1,684, Delhi 1,593, Noida 1,363, Bengaluru 1,196, Chandigarh 1,039, Balcony grill 876 in 39 h. The only reels near or over 1,000 reach (L17, Signal, 6 reels).
- Real case with a loss people fear (Mumbai no-OC): the only reel over 2 sends per 1,000 (26.1). Early sign, 1 reel.
- Regional heritage or small-place curiosity without a national hook: Ahmedabad pols 108 (skip 83.6%), Shani 112, Kerala 104, Jaipur 134. Now 4 reels, all under 140 reach: avoid as the IG reel unless the line ties it to every Indian city.
- Rules or money on a generic object: Flat or plot 119, Carpet 163, Mumbai rent 95, home loan 63. 4 reels, the weakest shape on IG.
- Engineering marvels and global comparisons (Aangan, Hong Kong, Steinway) are weak on IG (134 to 252) but lead YouTube (550, 437, 462).

### Looks and voices (early sign; the look test X3 closed 25 Nov with no look effect)
Look T is allowed, not required (D2 ended 25 Nov). Voices: Tara 7 reels, Jessa 8, George 6; Chandigarh (George) 38.8% and Balcony (Jessa) 38.2% show topic and opening decide, not the voice. Not tracked as a test.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 744, Steel rods 686, Aangan 550 (p89), Steinway 462 (p84), Hong Kong 437, Jakarta 223, Mumbai rent 145, Shani 129, Kerala 120, Chandigarh 112, Jaipur 104, Balcony 98, Japan 91, Flat or plot 70 and pols 63 (first day), Delhi 59, SC 21, Bengaluru 14, Burj 5. Subscribers 6 (+0). Engineering and global scale win YouTube; famous-India IG winners do less. Rule for reel runs (unchanged): YouTube title is the plain question plus the scale number, no puzzle wording; one engineering or scale story a week as the YouTube-first slot; judge by subscribers (D30). Mumbai no-OC still has no YouTube copy.
- Facebook: Steel rods 781, Kerala 282 (p96), Ahmedabad pols 253 in under a day (p93), Bengaluru 239, Burj 232, Jakarta 221, Steinway 216, Jaipur 215, Mumbai rent 203, Chandigarh 92, SC 77, Balcony 50, Flat or plot 37, Mumbai no-OC 25. Heritage and place stories (Kerala, pols, Jaipur) do better on Facebook than on IG. Rule for reel runs: Facebook text names the place and the year in line one and asks a memory question ("Have you walked a pol?"); Facebook gives about 200 plays to a place story, so it is a reach floor, not a judge. Page followers 7.
- Threads: stamp duty carousel 175, Kerala 105 (p96), cost-of-flat carousel 104 (p93), SC news 50, Bengaluru 44; reels 0 to 17. Rule stays: Threads text leads with the number and the place in line one; carousels go to Threads as a numbered text list.
- X: Bengaluru 27 (p100), Chandigarh 25 (p96), Steinway 18 (p93), Balcony 14 (p89), Carpet 13, Shani 12, Aangan 12, Mumbai no-OC 11, pols 11 (p75). A famous Indian place plus a puzzle in line one does best on X; no follows; text-only cross-posts are enough. Avoid bare domain names in X text (X auto-links them).
- Underperformed on IG but top 20% elsewhere: Ahmedabad pols (IG 108, skip 83.6%; FB p93), Steinway (IG 144; YT p84, X p93), cost-of-flat carousel (IG 18; Threads p93), Aangan (IG 252; YT p89), Kerala (IG 104; FB p96, Threads p96). Reverse: Balcony grill (IG 876; YT p42, Threads p36), Delhi (IG 1,593; YT 59), Bengaluru (IG 1,196; YT 14).
- Same everywhere: Steel rods top on IG, FB and YouTube; Bengaluru and Chandigarh top 20% on IG and X.

## Do more
- "Why does X look like this" on a thing on every Indian street (Steel rods, Balcony grill): 3 reels, median skip 38.2%, hold 42.2%, 11.6 points ahead of contradiction (L21). Make it at least 1 reel in 2 while it leads (D42, cheap and reversible).
- Contradiction on a FAMOUS Indian place or real case, city in the first line (Chandigarh 1,039 reach, skip 38.8%; L17).
- Real cases where buyers lost something (Mumbai no-OC: 26.1 sends per 1,000). Good shape for X19 shares reels: the family argument should sit inside a real case, not a generic object.
- Full-frame motion opening with the line spoken from 0 s (Proven, L18).
- 44 to 52 s length (Mumbai no-OC 44.8 s hold 28%, Balcony 51.2 s hold 52.8%).
- For YouTube: one engineering or global scale story a week (Aangan, Hong Kong, Steinway: 437 to 550 views). For Facebook: heritage and place stories travel (pols 253 in a day).

## Do less
- Rules or money explainers on a generic object (Flat or plot 119, skip 73.2%; Carpet 163; Mumbai rent 95; home loan 63). Put the rule inside a famous place or real case.
- Regional heritage or small-place curiosities as the IG reel (Ahmedabad pols 108, skip 83.6%; Shani 112; Kerala 104; Jaipur 134). Keep them for Facebook and YouTube only if made anyway.
- Text cards, label bars or a bare number as the first frame (median skip 80%).
- Reels over 55 s (every one since 19 Nov holds under 23%).
- Judging growth ads on cheap profile visits: all-India visits at INR 0.56 do not turn into more follows (see BOOST_LOG 26 Nov).

## Running experiments
- Hook tournament (X1): archetype 24 3 reels, median skip 38.2%, hold 42.2%; contradiction 12 reels, 49.8%, hold 22.3%. Gap 11.6 points, past the 10-point line: archetype 24 becomes the preferred hook for at least half the reels (Hunch L21, D42). Next review 2026-11-29 with the next two archetype 24 reels.
- Shares (X19, D56): shares reel 1 Flat or plot 119 reach, 0 sends at 21.5 h (skip 73.2%); control 1 Ahmedabad pols 108 reach, 0 sends at 14.5 h. Judged at 72 h; 1 of 4 per side. Benchmark: Mumbai no-OC 26.1 sends per 1,000. Note for the planner: a family-argument topic still needs the famous-place or real-case shape to get past 3 s.
- Follow outro (X15, D49): voiced Shani 16.9%, Bengaluru 15.7%, Chandigarh 21.0%, Balcony 52.8%, pols 7.1% hold; silent Carpet 17.1%, Steinway 18.2%, Mumbai no-OC 28.0%, Flat or plot 19.9%. 5 vs 4 reels; account follows per day do not separate them. Too early; outro does not cost hold.
- Length (X18): Mumbai no-OC 44.8 s hold 28.0%, Flat or plot 43.6 s hold 19.9%, against 56 to 60 s reels at 15.7 to 17.1%. 2 of 3 short reels.
- Grid not trial (D54, 23 to 30 Nov): 6 grid reels median skip 48.4% vs 53.1% for the last 11 trials (gap now 9%, was 22%); about 47 paid profile visits per new follower in the last 24 h (1 in 96 was the old bar) (target better than 1 in 96). L20 weakening; check ends 30 Nov.
- Geography (L2, L17): national India famous place or every street 876 to 1,684 IG reach (6 reels); global 134 to 422 (6 reels); regional or small-place India 104 to 163 (6 reels).
- Growth ads (X16, D55, warm test, judged today): see BOOST_LOG 26 Nov. Spread-only day (23 Nov, INR 234) +8 followers; the two days with both campaigns (24 and 25 Nov, about INR 960) +9 and +5. Adding the all-India campaign doubled spend with no extra follows, so the warm spread is the better campaign. Spread kept; asked Rishi to stop the all-India campaign (N65).
- Remixes queued (14-day rule): Delhi (Lutyens, Paris), Noida (minute-by-minute, Maradu), Steel rods (black tanks, one floor at a time, from 2 Dec), Kerala (akiya, Gulf mansions, from 4 Dec), Bengaluru (Chennai wetlands, Tehri, lake-bed plot check, from 6 Dec), Steinway (from 7 Dec, YouTube-first), Chandigarh, Mumbai no-OC and Balcony grill (from 8 Dec).

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
- 2026-11-26: both 25 Nov grid reels are early duds (Flat or plot, X19 shares reel 1, skip 73.2%; Ahmedabad pols skip 83.6%) because a rule on a generic object and a regional heritage topic do not stop a national audience, so the grid alone does not rescue a weak topic (L20 weakens); archetype 24 passes the X1 line (11.6 points ahead of contradiction, Balcony grill hold 52.8%, L21); pols is p93 on Facebook in a day; IG 444 (+5), FB 7, YT 6, Threads 12; warm test (D55) judged: spread-only day +8 vs +9 and +5 on days with both campaigns at double the spend, so spread is kept and the all-India campaign should stop (N65); Balcony grill added, Japan paused (ages out).
