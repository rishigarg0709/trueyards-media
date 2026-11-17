# Boost policy (set by Rishi, 2026-11-16)

- Budget: at most INR 5,000 per calendar month across all boosts. Typical boost INR 300 to 500 over 2 to 3 days.
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
- Keep at most 2 ads active and add at most 1 new ad per day. Rotate: pause an ad after 4 days or when a newer reel beats it.
- Prepaid funds: about INR 847 usable (INR 1,000 incl. GST), so about 8 days. When funds run low, tell Rishi to top up; never touch billing.
- Budget raised to INR 200/day by Rishi on 2026-11-17 (about INR 6,000 a month if it runs every day; the INR 5,000 monthly cap still applies).
