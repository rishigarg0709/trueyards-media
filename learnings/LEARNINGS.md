# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-20-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:14 UTC 20 Nov; 17 TrueYards posts on Instagram, the Forteasia reel excluded). Noida (since 18 Nov), Steel rods (since 19 Nov 13:26 IST) and Delhi (from 20 Nov 10:49 IST) are in the TrueYards Follow ad set: their Instagram post insights stay organic only; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level (Facebook does return a per-reel follower count).
- Followers: IG 412 (+0 in 24 h), FB page 6 (+1), YouTube 1 subscriber (+0; channel 1,970 views), Threads 11 (+1), X not returned. Progress to 100,000: 0.41%.
- Follows per 1,000 reach (account): 19 Nov had 8,041 IG reach (about 8,000 of it paid) and 0 new followers, so 0 per 1,000. The growth ad bought 446 profile visits for INR 200 and not one follow. Since the ad started (18 Nov 16:45): 620 visits, +4 followers, about 1 in 155 visitors follows. Funnel diagnosis: journey stage (the profile does not convert paid visitors). Alternative explanation: Meta's profile-visit optimisation finds accidental tappers who never read the profile; the new bio (19 Nov 14:15) has had only 1 full day.
- Best reel (still): Steel rods trial (18 Nov midday, 45 h): reach 1,651, skip 35.0%, hold 42.4%, likes 2.4%, 2 sends (1.2 per 1,000). Also top on Facebook (776 plays) and 669 YouTube views (63 s average view, the only Short watched past 100%). Not a D18 strong trial (hold 42.4% vs 45%, sends 1.2 vs 2 per 1,000); already on the grid.
- The two 19 Nov trials failed at the hook: Jaipur pink (midday, 21 h): reach 134, skip 64.0%, hold 16.5%, 0 sends, 0 likes. Mumbai rent (evening, 15 h, look T): reach 94, skip 81.7%, hold 10.7%, 0 likes. Both are dud signals (skip 60%+). Diagnosis: distribution stage caused by the hook (trials go to non-followers only, so a weak first 3 s means Instagram stops testing). Alternative explanation: Trial Reels now get a smaller first test than on 17 and 18 Nov.
- Trials so far (D18, compare with trials only): Steel rods 1,651 reach, skip 35.0%; Japan 401, 46.9%; Jaipur 134, 64.0%; Mumbai 94, 81.7% (15 h). Median reach 268, median skip 55.5%. The trials that worked opened on a real or photoreal object with a why or contradiction line; the two that failed opened on a year (1876) or a price (Rs 1,300).
- Off Instagram the weak IG reels hold up: Mumbai rent FB 200 plays and YT 134; Jaipur FB 197 plays and 1 FB follow (5 per 1,000 plays, the only per-post follow we can see).
- Sends remain the bottleneck: 4 sends on Instagram across all reels in 7 days (Delhi 2, Steel rods 2), 0 comments on any IG post.
- Carousels reach 2 to 11 accounts on Instagram (price myth 2, Expressway 8). Not distributed on IG; Threads is their channel.

### Hook tournament standings (IG reels, organic; ranked by skip because follows per post are not returned; early sign, no arm has 8 posts)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods trial) | 1 | 1,651 | 35.0% | 42.4% | 1.2 |
| 1 Contradiction (Delhi, Noida, Japan trial, Burj) | 4 | 3,605 | 45.4% | 32.7% | 0.6 |
| 10 Visual shock (Jakarta) | 1 | 182 | 55.7% | 16.5% | 0 |
| 14 Story cold open (Jaipur trial) | 1 | 134 | 64.0% | 16.5% | 0 |
| 2 Number slam (home loan; Mumbai rent trial) | 2 | 142 | 83.2% | 16.8% | 0 |
| Unlogged (15 Nov reel) | 1 | 147 | 72.2% | n/a | 0 |
Leader: archetype 24 on quality, contradiction on volume. Number slam has now failed twice as a reel opening (skip 84.6% and 81.7%): early sign, keep number slams for carousel slide 2, not reel frame 0.

### Story types (early sign)
- India stories still win on Instagram when the hook works: Steel rods 1,651, Delhi 1,562, Noida 1,336 vs global Japan 401, Burj 306, Jakarta 182. But the two India trials of 19 Nov (Jaipur 134, Mumbai 94) show the hook matters more than the geography. India median now 1,336 (5 posts) vs global 306 (3 posts).
- Everyday India (something every viewer has seen on their own street) is the best story type (Steel rods, 1 post). History (Jaipur) and money maths (Mumbai rent, home loan) are the weakest so far on IG.
- Real case with a buyer lesson gives saves (Noida 4); city puzzles and everyday mysteries give sends (Delhi 2, Steel rods 2).

### Looks and voices (early sign, 1 to 2 reels each)
| Look | Reels | Reach | Skip | Hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods trial) | 1 | 1,651 | 35.0% | 42.4% |
| A Newsroom Red, photoreal event (Delhi, Noida) | 2 | 2,898 | 43.8% | 35.6% |
| F Tokyo Neutral (Japan trial) | 1 | 401 | 46.9% | 31.5% |
| E Blueprint line art (Burj) | 1 | 306 | 59.3% | 24.0% |
| B Emerald Doc (Jaipur trial) | 1 | 134 | 64.0% | 16.5% |
| T TrueYards Brand (Jakarta, Mumbai rent trial) | 2 | 276 | 68.7% | 13.6% |
Look T test (D2, 18 to 25 Nov): 2 reels in, both the weakest of their slot (median skip 68.7% vs 53.1% for all other reels); the look T carousel (price myth) reached 2 on IG. Confounded with hook (visual shock, number slam) and topic, so not proven, but look T has not yet won anything on IG. On Facebook look T does fine (Jakarta 216, Mumbai 200 plays).
Voices: Tara (Noida, Steel rods, Mumbai rent) median skip 43.7%; Jessa (Delhi, Japan, Jakarta) 46.9%; George (Burj, Jaipur) 61.7%. Confounded with topic.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 735 views (top, 40 s average, 73% of length), Steel rods 669 (63 s average, 120%: rewatched), Jakarta 217, Mumbai rent 134, Japan 91, Jaipur 75, Delhi 52, Burj 5. YouTube rewards India real-case and everyday-India stories with a plain title. Rule for reel runs: YouTube title = plain event plus stakes ("Why Indian houses have steel rods on the roof"), no puzzle wording. Judge YouTube by subscribers (still 1) and site visits (D28 second).
- Facebook: Steel rods 776 plays, Burj 231, Jakarta 216, Mumbai rent 200, Jaipur 197; Noida 3, Japan 7. Every reel posted since 17 Nov evening gets about 200 plays on Facebook whatever its IG result; average watch 1.6 to 5.8 s. Facebook is a reach floor, not engagement (4 reactions in total). Jaipur gave the first FB follow.
- Threads: stamp duty carousel 175 views, the SC stalled-loans news post 35 (20 Nov), reels 1 to 16. Text-first money facts and news win. Rule for carousel runs: every carousel goes to Threads with a 2 to 3 line text hook naming the number and the cities (the price myth carousel got 13 and Expressway 11 with weaker first lines).
- X: 0 to 8 views per post, no engagement. Not a growth channel; text-only cross-posts, no X-specific effort.
- Underperformed on IG but top 20% elsewhere: Mumbai rent (IG 94, FB 200 p77, Threads 16 p83), Jakarta (IG 182, FB 216 p85, YT 217 p75), Burj (IG 306, FB 231 p92), stamp duty carousel (IG 11, Threads 175 p100). Reverse: Delhi (IG 1,562, YT 52, Threads 11).

## Do more
- Open every reel on a bright real or photoreal object the viewer recognises, with a why or contradiction line (Steel rods trial 35% skip, contradiction median 45.4%); queue re-ranked toward these.
- Everyday India things people see but never question (Steel rods: best reel on every metric, top on FB, rewatched on YT). Shani Shingnapur, aangan courtyards and Mumbai's black-stained towers are next in the queue.
- Follow conversion: paid visitors do not follow (446 visits, 0 follows on 19 Nov). The first 3 grid tiles must be the strongest reels (Steel rods, Delhi, Noida) and the Start here carousel (20 Nov 17:13) should be pinned so a visitor sees the promise at once.
- Carousels: first line on Threads states the money number and the cities (stamp duty 175 vs price myth 13).

## Do less
- Number slam as the first frame of a reel (home loan skip 84.6%, Mumbai rent 81.7%); keep the number for second 3 to 5 or carousel slide 2.
- Year-led story cold opens without a visual question (Jaipur 1876: skip 64%).
- Dark or line-art openings (Burj Blueprint 59.3%; the dark steel rods main 63.9% before deletion). D1 brightness rule stands.
- Look T on reels until it wins once: 2 of 2 look T reels are the weakest of their slot (Directive D2 test still runs to 25 Nov, so keep using it for one reel a day, but pair it with a proven hook so the look is the only change).
- Posting without a log.md entry (15 Nov reel still cannot be scored).

## Running experiments
- Hook tournament (X1, weeks 1 to 4): standings above; next review 2026-11-23. Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels (archetype 24 is 10.4 points better on 1 reel; number slam 38 points worse on 2).
- Trial first (D18, from 19 Nov): trials compared only with trials (median of the last 10; now 4 trials, median reach 268, skip 55.5%). No trial meets the strong-trial bar (skip under 35%, hold 45%+, sends or follows 2+ per 1,000) today.
- Look T (X3, D2, 18 to 25 Nov): 2 of 5 reels in (Jakarta skip 55.7%, Mumbai rent 81.7%; median 68.7% vs 53.1% for the rest). Review 2026-11-25 on trials only. Next look T reel should use a contradiction or archetype 24 hook so the look is the single change.
- Geography: India vs global on IG, 5 vs 3 posts, India median 1,336 vs 306 reach. Next: one global topic as a midday trial with a bright photo and a why hook (Hong Kong today).
- Reel length: all reels are 47 to 57 s. Still need one 35 to 45 s reel.
- Platform titles: plain event titles on YouTube, number-first Threads text for carousels. Review 2026-11-21.
- Growth ads (X4): TrueYards Follow, INR 200/day, profile-visit goal, now 3 reels in one ad set (D28). Since 18 Nov 16:45: INR 289.56, 620 profile visits (INR 0.47 each), +4 followers (about INR 72 each gross, 155 visits per follower). 19 Nov: INR 200, 446 visits, 0 follows. Meta gives Noida all the spend (Steel rods INR 0.07). Formal check against INR 12 per follower in the 22 Nov run.
- Posting slot: midday vs evening. Midday Delhi 1,562, Japan 401, Steel rods 1,651, Jaipur 134; evening Noida 1,336, Burj 306, Jakarta 182, Mumbai rent 94. Midday median 982 vs evening 244; confounded with hooks and topics.
- Remixes queued (14-day rule): Delhi (Lutyens cold open, Paris), Noida (minute-by-minute retelling, Maradu), Steel rods (black water tanks, building one floor at a time, from 2 Dec).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
- 2026-11-20: the 19 Nov trials failed at the hook (Jaipur cold open skip 64%, 134 reach; Mumbai rent number slam skip 81.7%, 94 reach); number slam openings now 2 of 2 failures; look T 2 of 2 weakest; growth ad spent INR 200 for 446 profile visits and 0 follows (IG flat at 412), Delhi added as a third ad; every reel gets about 200 Facebook plays regardless of IG.
