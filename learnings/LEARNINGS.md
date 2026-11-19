# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-19-media.csv, -account.csv, -facebook.csv, -cross.csv, -platforms.csv (pull 05:11 UTC 19 Nov; 14 TrueYards posts on Instagram, the Forteasia reel excluded). The deleted 17 and 18 Nov main reels are gone from the data; their trial versions (now on the grid) are what we score. Noida is boosted since 18 Nov 05:14 UTC: Instagram post insights stay organic only, so its post numbers below are organic; ad numbers live in BOOST_LOG.md. Reels do not return follows or profile visits per post, so follows per 1,000 reach is measured at account level.
- Followers: IG 412 (+4 in 24 h, the first day with growth ads), FB page 5 (+1), YouTube 1, Threads 10, X not returned. Progress to 100,000: 0.41%.
- Follows per 1,000 reach (account): 18 Nov window had about 2,000 organic reach plus about 5,400 paid reach and +4 followers, so about 0.5 per 1,000 total reach and at most 2 per 1,000 organic. Still far below the 2 to 5 typical line. The ad bought 229 profile visits for INR 107 (INR 0.47 each) but only about 4 of 229 visitors followed (under 2%). Funnel diagnosis: distribution and profile visits now work; the profile itself does not convert (journey stage). Alternative explanation: one day, and the follower count lags.
- Best reel so far: Steel rods trial (18 Nov midday, 21 h): reach 1,635, skip 34.8% (best ever, first under 35%), hold 42.5% (22.1 s of 52.0 s, best ever), likes 2.4% (first big reel above the 2% weak line), 2 sends (1.2 per 1,000), 1 save. Also top on Facebook (624 plays, 3x any other) and 640 YouTube views. Bright real rooftop photo on frame 0 plus a "why does X look like this" question. Not a D18 strong trial yet (hold 42.5% vs the 45% bar, sends 1.2 vs 2 per 1,000); it is already on the grid.
- Jakarta sinking (18 Nov evening, 14.5 h, first look T reel): reach 169, skip 55.6%, hold 16.8% (9.2 s of 55.0 s), likes 1.8%, 1 save. Weak on Instagram at 14 h (it was a normal reel, not a trial, so it started with our followers). Off Instagram it did well: YouTube 203 views (5 likes), Facebook 214 plays. Hook diagnosis: low hold plus normal views/reach (1.11) = the first seconds lost people. Confounds: evening normal post vs midday trial, global topic, new look.
- Late growth on Instagram for the 17 Nov reels: Burj 168 to 305 reach and Japan trial 363 to 400 in 24 h, so global reels pick up slowly; still 4x behind the India reels.
- Sends remain the bottleneck: 4 sends on Instagram across all reels in 6 days (Delhi 2, Steel rods 2). 0 comments on any IG post. Saves: Noida 4, others 0 to 1.
- Carousels still reach 7 to 10 accounts on Instagram (Expressway 7). Not distributed. Stamp duty carousel now 174 Threads views.

### Hook tournament standings (IG reels, organic; ranked by skip, as follows per post are not returned; early sign, no arm has 8 posts)
| Archetype | Posts | Reach | Median skip | Median hold | Sends per 1,000 |
|---|---|---|---|---|---|
| 24 Why does X look like this (Steel rods trial) | 1 | 1,635 | 34.8% | 42.5% | 1.2 |
| 1 Contradiction (Delhi, Noida, Japan trial, Burj) | 4 | 3,598 | 45.4% | 33% | 0.6 |
| 10 Visual shock (Jakarta, 14 h) | 1 | 169 | 55.6% | 17% | 0 |
| 2 Number slam (home loan, 24 s, old rules) | 1 | 46 | 88% | 23% | 0 |
| Unlogged (15 Nov reel) | 1 | 146 | 72.7% | n/a | 0 |
| Myth bust, stakes, story cold open, versus, hidden in plain sight (17 as a main was deleted), counterintuitive economics (main deleted) | 0 | | | | |
Leader: contradiction on volume (4 posts), archetype 24 on quality (1 post). Today's Jaipur reel tests 24 again; if it also beats a 40% skip, archetype 24 becomes the second leader.

### Story types (early sign)
- India stories win on Instagram: Steel rods 1,635, Delhi 1,562, Noida 1,331 vs global Japan 400, Burj 305, Jakarta 169. Three posts each side now; India median 1,562 vs global 305 (5x). Still confounded with look and slot.
- Everyday India (something every viewer has seen on their own street) gave the best skip, hold and likes of any reel. One post, early sign.
- Real case with a buyer lesson gives saves (Noida 4); city puzzles and everyday mysteries give sends (Delhi 2, Steel rods 2).

### Looks and voices (early sign, 1 to 2 reels each)
| Look | Reels | Reach | Skip | Hold |
|---|---|---|---|---|
| C Midnight Gold with bright real photos (Steel rods trial) | 1 | 1,635 | 34.8% | 42.5% |
| A Newsroom Red, photoreal event (Delhi, Noida) | 2 | 2,893 | 43.7 to 44% | 34 to 37% |
| F Tokyo Neutral (Japan trial) | 1 | 400 | 46.9% | 32% |
| T TrueYards Brand (Jakarta, 14 h) | 1 | 169 | 55.6% | 17% |
| E Blueprint line art (Burj) | 1 | 305 | 59.5% | 24% |
Look T test (D2, 18 to 25 Nov): 1 of 5 reels in; weakest-but-one on IG so far, but its only reel was a global evening normal post. Judge look T on trials only from today; compare with the trial median (currently Japan 400 and Steel rods 1,635 reach, skip 46.9% and 34.8%).
Voices: Tara (Noida, Steel rods) median skip 39%; Jessa (Delhi, Japan, Jakarta) 46.9%; George (Burj) 59.5%. Confounded with topic.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida 728 views (top), Steel rods 640, Jakarta 203, Japan 89, Delhi 53, Burj 5. Engagement per view: Noida 1.9%, Steel rods 2.2%, Jakarta 2.5%. YouTube rewards India real-case and everyday-India stories with a plain title, and gave the IG-weak Jakarta its best audience after Facebook. Rule for reel runs: YouTube title = plain event plus stakes ("Why Indian houses have steel rods on the roof"), no puzzle wording.
- Facebook: Steel rods 624 plays, Burj 229, Jakarta 214; Noida 3, Japan 6, Delhi none. Average watch 3 to 6 s. Facebook likes engineering and global marvels plus everyday India; it ignores court cases. Early sign (3 posts above 200). Only 3 reactions across all FB reels; FB is reach, not engagement.
- Threads: stamp duty carousel 174 views vs 1 to 15 for every reel. Text-first money facts win; reels on Threads stay low priority. Rule for carousel runs: every carousel goes to Threads with a 2 to 3 line text hook naming the number and the cities. The Expressway carousel got only 7 on Threads, so the number plus named cities in the first line matters (its first line was a promise, not a money number).
- X: 1 to 8 views per post, no engagement. Not a growth channel; text-only cross-posts, no X-specific effort.
- Underperformed on IG but top elsewhere: Jakarta (IG 169, YT 203 and FB 214), Burj (IG 305, FB 229), stamp duty carousel (IG 10, Threads 174). Reverse: Delhi (IG 1,562, YT 53, Threads 10).

## Do more
- Everyday India things people see but never question, with a bright real photo of the thing on frame 0 and a why question (Steel rods trial: skip 34.8%, hold 42.5%, likes 2.4%, top on FB and second on YT). One post, early sign, but it beats every other reel on every metric.
- India stories over global for Instagram (median 1,562 vs 305 reach, 3 posts each). Keep global stories for variety, and push them on YouTube and Facebook where they do well.
- Contradiction hook with a photoreal event on frame 0 (4 posts, median skip 45%): the safe default.
- Follow conversion: the growth ad sends cheap profile visits (INR 0.47) that do not follow (under 2%). Every reel ends with the follow card (D9), and the first 3 grid tiles should be the strongest reels (Steel rods, Delhi, Noida) so a visitor sees what they get.
- Carousels: first line on Threads states the money number and the cities (stamp duty 174 vs Expressway 7).

## Do less
- Dark or line-art openings (Burj Blueprint skip 59.5%; the steel rods main with a dark silhouette had skip 63.9% before deletion). D1 brightness rule stands.
- Long global explainers posted as normal (non-trial) evening reels: Jakarta 169 and Burj 168 at 15 h. From 19 Nov every reel is a trial (D18), which should fix the follower-first weak test.
- Short money-maths reels without a story (home loan reel: skip 88%, reach 46).
- Rishi disliked and deleted the 2026-11-16 carousel "Your EMI didn't change. Your loan did." (text-heavy middle slides without the big 3D models and still-life objects). See PLAYBOOK.md visual richness rules.
- Posting without a log.md entry (15 Nov reel still cannot be scored).

## Running experiments
- Hook tournament (X1, weeks 1 to 4): standings above; next review 2026-11-23. Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels (archetype 24 is 10.6 points better on 1 reel).
- Trial first (D18, from 19 Nov): compare trials only with trials (rolling median of the last 10). Trials so far: Japan 400 reach, skip 46.9%; Steel rods 1,635, skip 34.8%. Flag any trial at 24 h with skip under 35%, hold at least 45% and sends or follows of 2 or more per 1,000 that is not on the grid.
- Look T (X3, D2, 18 to 25 Nov): 1 of 5 reels in (Jakarta, weak on IG, decent on YT and FB). Review 2026-11-25 on trials only.
- Geography: India vs global on IG, 3 posts each, 5x gap in median reach. Next: one global topic as a midday trial with a bright photo opening, to separate topic from slot and look.
- Reel length: all reels are 47 to 57 s. Still need one 35 to 45 s reel.
- Platform titles: plain event titles on YouTube, number-first Threads text for carousels. Review 2026-11-21.
- Growth ads (X4): TrueYards Follow, INR 200/day, profile-visit goal. Day 1: INR 107 spent, 229 profile visits (INR 0.47 each), about 4 new followers. Old engagement boost (18 Nov, INR 47): 2,893 reached, 312 likes, about 2 follows. Review cost per new follower at INR 1,400 spent (about 25 Nov). Next ad: Steel rods trial from 13:17 IST 19 Nov (24 h rule).
- Posting slot: midday vs evening. Midday Delhi 1,562, Japan trial 400, Steel rods trial 1,635; evening Noida 1,331, Burj 305, Jakarta 169. Midday leads (median 1,562 vs 305), but midday reels were trials and India topics; confounded.
- Remixes queued (14-day rule): Delhi (Lutyens cold open, Paris), Noida (minute-by-minute retelling, Maradu), Steel rods (from 2 Dec).

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
- 2026-11-19: Steel rods trial is the best reel on every metric (skip 34.8%, hold 42.5%, 1,635 reach, top on FB with 624 plays); Jakarta (first look T reel) weak on IG (skip 55.6%, 169 reach) but 203 YT and 214 FB; India median reach 5x global; first growth-ad day: 229 profile visits for INR 107 but only about 4 new followers (412), so profile conversion is the new bottleneck.
