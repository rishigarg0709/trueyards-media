# Boost policy (set by Rishi, 2026-11-16)

- Budget: at most INR 5,000 per calendar month across all boosts. Typical boost INR 300 to 500 over 2 to 3 days.
- Goal: profile visits (Meta engagement campaign, ad set destination FACEBOOK_PAGE with optimization_goal PROFILE_AND_PAGE_ENGAGEMENT and call_to_action_type VISIT_PROFILE, via Windsor boost_post).
- Only boost posts already winning organically: top 1 or 2 from learnings/BOOST_CANDIDATES.md (shares per reach and skip rate clearly better than the account median, at least 48 h old).
- Autopilot (Rishi, 2026-11-16): one always-on campaign "TrueYards Boost" with a fixed daily budget of INR 160 (about INR 4,900 a month), approved once by Rishi. The daily learning run may only add the best 1 or 2 qualifying posts as ads and pause fading ones inside that campaign. It must never raise the budget, create another spending campaign or ad set, or change billing. Budget changes happen only when Rishi asks in chat.
- Audience: India, ages 22 to 50, interests in real estate, home buying, personal finance, architecture; exclude existing followers when possible.
- Never boost Forteasia or FIT project content from TrueYards.
- After each boost, record spend, profile visits, follows gained and cost per follow in learnings/BOOST_LOG.md. Stop boosting a format if cost per follow is more than 3x the median.
- Runs on GitHub Actions with Rishi's Meta system-user token (secret META_TOKEN), no laptop needed. A spend cap check in code refuses any change that would push month-to-date spend past INR 5,000.
- Weekly spend, follows gained and cost per follow go in the Monday learning message.
