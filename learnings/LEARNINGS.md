# What's working on TrueYards (auto-updated daily)

Every reel and carousel run reads this file before choosing a topic, hook and style. The daily analytics run rewrites the "Current findings" section from real Instagram data. Rules in REEL_HOOKS_PLAYBOOK.md and learnings/VIRALITY_PLAYBOOK.md still apply; this file decides priorities within them, using our own data.

## How posts are scored (only posts at least 48 h old)
- Reels: skip rate (share of viewers who leave in the first 3 s, lower is better), average watch time as a share of reel length, shares per 1,000 reach, saves per 1,000 reach, reach from non-followers.
- Carousels: shares and saves per 1,000 reach, follows from the post, profile visits.
- Account: new followers per day, non-follower reach.
- Compare each post with the account's rolling median, not with absolute numbers. Call something a pattern only when it holds across at least 3 posts.

## Current findings
Data: learnings/data/2026-11-18-media.csv, -cross.csv, -facebook.csv, -platforms.csv (pull 05:11 UTC 18 Nov, 13 TrueYards posts plus 1 excluded Forteasia reel). Still no post final at 72 h except the 14 Nov carousels and home loan reel. No TrueYards ad had run before this pull, so every number below is organic. Noida is boosted from 05:14 UTC 18 Nov: from tomorrow its numbers are tagged boosted and kept out of organic scoring.
- Followers: IG 408 (0 change on 17 Nov despite 1,749 account reach), FB page 4, YouTube 1 subscriber, Threads 10, X not returned. 30-day account reach 4,694, only 17 from followers.
- Reels plateau after about 24 h. Delhi 1,545 to 1,560 and Noida 1,301 to 1,326 in the last 24 h (+1% and +2%). Judge reels at 24 h for distribution; the 72 h mark mostly confirms.
- Japan houses (17 Nov midday, 21 h): main 186 reach, skip 50.0%, hold 29% (15.6 s of 53.1 s), 1 save. Trial twin 363 reach, skip 47.7%, hold 33% (17.4 s), 0 saves. First trial pair: the contradiction hook (trial) beat counterintuitive economics (main) on reach (2x), skip (2.3 points) and hold (4 points). One pair, early sign.
- Burj Khalifa on sand (17 Nov evening, 15 h): reach 168, skip 63.8%, hold 20% (9.7 s of 47.6 s), likes 2.4%. Weakest new-rule reel on Instagram. Hook diagnosis: low hold plus normal views/reach (1.20) = hook and first seconds lost people. Changed vs Delhi and Noida: look E Blueprint (dark navy line art instead of a photoreal event), voice George, global topic, shorter 47.6 s. Alternative explanation: 15 h is early, and the evening slot after a midday reel plus trial twin may have split distribution.
- Engagement is the bottleneck everywhere. Best IG likes per reach on a big reel is 1.0 to 1.6% (weak line is 2%); sends per reach 0 to 0.13% across all reels; 0 comments on any IG post. Follows per 1,000 reach about 1 (5 follows on 16 Nov from 2,880 reach, 0 on 17 Nov from 1,749). Funnel: distribution works for photoreal India stories, message and journey stages do not.
- Carousels still reach 6 to 9 accounts on Instagram (stamp duty 6). Not distributed; keep judging them on Threads and saves.

### Hook tournament standings (IG reels, organic; early sign, no arm has 8 posts)
| Archetype | Posts | Reach | Median skip | Median hold | Sends/reach |
|---|---|---|---|---|---|
| 1 Contradiction (Delhi, Noida, Japan trial twin, Burj) | 4 | 3,417 | 45.8% | 33.5% | 0.06% |
| 25 Counterintuitive economics (Japan main) | 1 | 186 | 50.0% | 29% | 0% |
| 2 Number slam (home loan, 24 s, old rules) | 1 | 44 | 87.5% | 23% | 0% |
| Unlogged (15 Nov reel) | 1 | 144 | 72.0% | n/a | 0% |
| Myth bust, stakes, story cold open, visual shock, versus, why does X look like this, hidden in plain sight | 0 | | | | |
Leader so far: contradiction (4 posts, 3,417 reach; it also won the first head-to-head twin). Today's queued reels test 17 hidden in plain sight (midday) and 10 visual shock (evening).

### Story types (early sign)
- Famous Indian place or case with a dramatic event (Delhi 1,560, Noida 1,326) beats global stories (Japan 186 plus 363 twin, Burj 168) on Instagram reach by about 4x so far. Two posts each side; topic, look and voice are confounded.
- Saves come from a real case with a buyer lesson (Noida 4 saves, Japan 1); sends only from the city puzzle (Delhi 2).
- Money maths without a story is last (home loan 44 reach).

### Looks and voices (early sign, 1 to 2 reels each)
| Look | Reels | Reach | Skip | Hold |
|---|---|---|---|---|
| Newsroom red, photoreal event (Delhi, Noida) | 2 | 2,886 | 43.5 to 43.9% | 34 to 38% |
| F Tokyo Neutral (Japan main + twin) | 2 | 549 | 47.7 to 50% | 29 to 33% |
| E Blueprint line art (Burj) | 1 | 168 | 63.8% | 20% |
Voices: Jessa (Delhi, Japan) and Tara (Noida) skip 43 to 50%; George (Burj) 63.8%, one reel, confounded with the Blueprint look.

## Platform fit (compare within a platform only)
- YouTube Shorts: Noida twin towers is the channel's top Short by far: 633 views, 11 likes, 3 comments (engagement per view 2.2%, top on YT) vs Japan 74, Delhi 50, Burj 4. On Instagram Noida was second. Early sign: YouTube rewards the dramatic real-case story with a clear event (court order, demolition) and title-style hook. Rule for the reel runs: YouTube Short titles name the event and stakes plainly ("Why India's Supreme Court ordered two towers blown up"), not the IG puzzle wording.
- Threads: the stamp duty carousel got 148 views vs 5 to 15 for every reel cross-post. On Instagram it reached 6. Early sign: Threads prefers text-first money facts (number plus named cities) over video. Rule for the carousel runs: post every carousel to Threads with a 2 to 3 line text hook that states the number and the cities; reels on Threads stay low priority.
- Facebook: Burj Khalifa got 220 plays (avg 4.6 s), the only FB reel above 10; Noida 1, Japan 5. Burj was our weakest reel on Instagram. Early sign: Facebook favours global marvel or engineering topics; one post.
- X: 1 to 8 views per post, no engagement. Not a growth channel yet; keep cross-posting text only (cheap) and do not spend effort on X-specific edits.
- Underperformed on IG but top elsewhere: Burj (IG 168 reach, top on FB), stamp duty carousel (IG 6, top on Threads). Reverse: Delhi (top on IG, 50 views on YT, 10 on Threads).

## Do more
- Contradiction hook with a photoreal built event on frame 0 and the hook number on screen (Delhi, Noida, Japan trial twin: skip 43.5 to 47.7%). It also won the first trial pair (363 vs 186 reach). 4 posts, early sign; keep testing other archetypes against it.
- Famous Indian place or real case with a dramatic event (Delhi 1,560 and Noida 1,326 reach vs 168 to 363 for global topics). Two posts each side, early sign.
- Photoreal imagery for the first 3 s, not line art or neutral flat looks (Newsroom red skip 44% vs Blueprint 64%).
- Sendable and followable endings: one line naming the person to send it to, then a series promise ("Part 2: how to check your own builder") to turn reach into follows. Follows per 1,000 reach are about 1.
- Carousels: write them so the Threads text works on its own (stamp duty: 148 Threads views).

## Do less
- Rishi disliked and deleted the 2026-11-16 carousel "Your EMI didn't change. Your loan did." (dark green, text-heavy, hourglass and house model, RBI repo explainer). Why (Rishi): unlike the first carousels it lacked the big Gemini 3D models and still-life objects on nearly every slide, crossing slide edges; the middle slides were text-only. See PLAYBOOK.md visual richness rules.
- Line-art or diagram-first openings (Burj Blueprint: skip 63.8%, hold 20%). One reel, early sign; if a blueprint look is used again, open on the photoreal subject and bring the line work in after 3 s.
- Short money-maths reels without a story (home loan reel: 24 s, skip 87.5%, reach 44).
- Posting without a log.md entry (15 Nov reel DfxHQD6vKff still cannot be scored).

## Running experiments
- Hook tournament (weeks 1 to 4): number slam, contradiction, stakes, myth bust, story cold open, visual shock, versus, why does X look like this, plus 17 and 25 as tested. Standings above; review weekly (next 2026-11-23). Changes our mind: any archetype beating contradiction on median skip by 10 points over 3 or more reels.
- Trial twins (midday): trial beat main in 2 of 2 pairs. Japan: 391 vs 186 reach. Steel rods (18 Nov, 12 h): trial 1,543 reach, skip 34%, avg watch 22.6 s vs main 136 reach, skip 63.9%, 10.1 s. Body identical from 3.9 s, so the gap is hook plus audience. Reasons: (1) trial goes to non-followers only, and our 411 followers barely engage, so main reels get a weak first test and stall (mains were 1,300 to 1,560 on 16 Nov before twins began, then 136 to 249); (2) the twin posted in the same minute splits the first-hour signal; (3) steel rods trial opened bright on real rooftops with a question, the main opened on a dark silhouette. 18 Nov 20:07 IST Rishi deleted the main reels and shared the trial versions to the main grid.
- Look: photoreal Newsroom vs Tokyo Neutral vs Blueprint (table above). Next: one global topic in the photoreal Newsroom look, to separate look from topic.
- Geography: India vs global on IG (2,886 vs 717 reach across 2 posts each). Confounded with look; same fix as above.
- Reel length: 35 to 45 s vs 46 to 55 s. All reels so far are 47 to 57 s; still need a 35 to 45 s reel.
- Platform titles: plain event plus stakes titles on YouTube (from Noida); text-first number hooks on Threads (from stamp duty). Review 2026-11-21 with 6 more posts.
- Boost (from 18 Nov): Noida twin towers boosted at INR 200/day. Measure cost per follow from daily IG follower change; organic baseline about 1 follow per 1,000 reach.
- Posting slot: midday vs evening. Midday Delhi 1,560, Japan 186 plus twin 363; evening Noida 1,326, Burj 168. No difference yet.
- Delhi remix topics stay queued (Lutyens cold open, Paris contradiction, Delhi height-rules carousel), first no sooner than 14 days after Delhi.

## History
- 2026-11-16: file created.
- 2026-11-17: first daily learning run. Delhi and Noida reels reached 1,545 and 1,301 (skip 44%) vs 42 to 142 before; sends are the bottleneck (0.13% and 0%); carousels stuck at 6 to 7 reach; contradiction leads the hook tournament (early sign, 2 reels); no boost (no eligible post 2 to 10 days old), campaign kept paused.
- 2026-11-18: reels plateau after 24 h (Delhi 1,560, Noida 1,326); first trial pair won by contradiction (Japan twin 363 vs main 186 reach); Burj weakest on IG (skip 63.8%) but top on Facebook (220 plays); Noida top on YouTube (633 views), stamp duty carousel top on Threads (148); followers flat at 408; first boost live (Noida, INR 200/day).
