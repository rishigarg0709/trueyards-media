# Boost policy (set by Rishi, 2026-11-16)

- Budget: at most INR 6,200 per calendar month across all boosts (raised from 5,000 by Rishi on 19 Nov 2026 so INR 200 a day is never cut off in a 31-day month). Typical boost INR 300 to 500 over 2 to 3 days.
- Goal: profile visits wanted, but Meta does not allow profile-visit ads on the new account yet, so the ad set optimises for post engagement (same as Instagram's Boost button). Retry profile visits later (Meta engagement campaign, ad set destination FACEBOOK_PAGE with optimization_goal PROFILE_AND_PAGE_ENGAGEMENT and call_to_action_type VISIT_PROFILE, via Windsor boost_post).
- Only boost posts already winning organically: top 1 or 2 from learnings/BOOST_CANDIDATES.md (shares per reach and skip rate clearly better than the account median, at least 48 h old).
- Autopilot (Rishi, 2026-11-16): one always-on campaign "TrueYards Boost" with a fixed daily budget of INR 100 (raised to INR 200 by Rishi on 2026-11-17) (started 2026-11-16 with INR 1,000 prepaid; Rishi tops up), approved once by Rishi. The daily learning run may only add the best 1 or 2 qualifying posts as ads and pause fading ones inside that campaign. It must never raise the budget, create another spending campaign or ad set, or change billing. Budget changes happen only when Rishi asks in chat.
- Audience: India, ages 22 to 50, interests in real estate, home buying, personal finance, architecture; exclude existing followers when possible.
- Never boost Forteasia or FIT project content from TrueYards.
- After each boost, record spend, profile visits, follows gained and cost per follow in learnings/BOOST_LOG.md. Stop boosting a format if cost per follow is more than 3x the median.
- Runs on GitHub Actions with Rishi's Meta system-user token (secret META_TOKEN), no laptop needed. A spend cap check in code refuses any change that would push month-to-date spend past INR 5,000.
- Weekly spend, follows gained and cost per follow go in the Monday learning message.

## Always-on growth spend (Rishi, 2026-11-17: "start spending organic growth money from tomorrow")
- From 18 Nov 2026 the campaign runs every day: keep at least 1 ad active at all times until the account reaches 1,000 followers, so the INR 100/day is actually spent (about INR 3,000 a month, inside the INR 5,000 cap).
- Eligible posts: organic TrueYards reels at least 24 h old (was 48 h) and at most 10 days old. Pick the best by reach, hold ratio, skip rate and sends per reach. If none is clearly top 10%, still boost the best eligible reel; pause_all only if there is no eligible TrueYards reel at all.
- Several reels at once, one shared ad set (Rishi, 19 Nov 2026 18:47: "who said to just run ad on one reel at a time ... make sure learning across reels is shared"). Keep 2 to 3 ads active inside the single "TrueYards Follow" ad set, on the same INR 200 a day, and add at most 1 new ad per day. One ad set means Meta's learning about who visits and follows is shared by every reel, and Meta splits the budget toward the reel that earns visits. Never create a second ad set or campaign, and never pause an ad only to push budget to another one. Pause an ad after 4 days, when its post is older than 10 days, or when it clearly loses on cost per new follower.
- Visit quality (learning L12, 19 Nov): the first INR 187 bought 456 profile visits at INR 0.41 each but only about 4 follows, under 1 in 100. Meta finds people who tap, and many taps are casual. Judge every ad and the campaign on follows, never on visits or cost per visit; report visits to follows in every run. If the campaign is above INR 12 per new follower after 2 full days on the new bio (from 20 Nov), say so to Rishi with a proposed change instead of continuing unchanged.
- Prepaid funds: about INR 847 usable (INR 1,000 incl. GST), so about 8 days. When funds run low, tell Rishi to top up; never touch billing.
- Budget raised to INR 200/day by Rishi on 2026-11-17 (about INR 6,000 a month if it runs every day; the INR 5,000 monthly cap still applies).

## Followers first (Rishi, 2026-11-18 16:33: "following is the goal", requirement 100k followers)
- 18 Nov 16:45: new campaign "TrueYards Follow" (traffic objective, optimised for Instagram profile visits, Instagram placements only: feed, reels, explore home; CTA View Instagram profile), same INR 200/day. The old engagement campaign "TrueYards Boost" is paused (its day: INR 46, 2,578 reached, 280 likes, about 2 follows).
- boost_post now adds ads to "TrueYards Follow" (config boost_campaign_name). Judge boosts on cost per new follower (follower change on boosted days vs organic days), then profile visits; likes do not count.
- The INR 5,000 monthly cap covers both campaigns together.

## Spread across reels (Rishi, 21 Nov 2026 12:14, Directive D40; replaces the single shared ad set of D28)
"I see only one video being boosted and getting views. It creates an artificial view that a video is being boosted, distribute the ads."
- Campaign "TrueYards Follow - spread" (no campaign budget): one ad set per reel with its own daily budget, so Meta cannot pour everything into one reel. The old "TrueYards Follow" (single ad set, Noida got about all of it) was paused on 21 Nov 12:20.
- Meta refuses a profile-visit ad set under about INR 95 a day, so the INR 200 funds 2 reels at INR 100 each.
- Rotation, every daily run: each reel gets paid exposure for 2 days, then hands over. Pick the 2 eligible reels (24 h to 10 days old, organic TrueYards, not project content) with the LEAST paid spend so far, breaking ties by the better skip rate; skip a reel whose organic skip rate is over 75% (money wasted on a hook that loses viewers). Prefer reels on the grid over trials that have not graduated. Run it with meta_ops op follow_spread {"media_ids": [id1, id2]}: it creates or keeps those 2 ad sets and pauses the others.
- Already had their paid turn before 21 Nov: Noida twin towers (about INR 600), Steel rods (about INR 0), Delhi skyscrapers (about INR 0). Steel rods and Delhi may get a 2-day turn like any reel.
- Judge on new followers per INR as before; log each run in BOOST_LOG.md.
