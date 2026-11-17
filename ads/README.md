# FIT Ads agent v1 (performance)

Meta click-to-WhatsApp ads from the TrueYards Facebook page (dark ads, not on the TY feed) into the FIT WhatsApp bot (+91 92206 07264). Brief: `strategy/PERFORMANCE_MARKETING_BRIEF.md` in the Forteasia x TY Claude Project. Separate from the organic agent and from the "TrueYards Boost" campaign: never touch either from here.

North star: cost per site visit done, then cost per booking, against brokerage earned.

## Files
- `config/ads.json`: account, caps, targets, ad sets, ad copy. Caps and `budget_approved` / `launch_approved` change only when Rishi says so in chat.
- `scripts/ads_ops.py`: all Meta calls and every rule. Workflow `.github/workflows/ads-ops.yml`.
- `ads/creatives/`: ad images, 2160 x 2700, both HRERA numbers top right.
- `ads/requests/<name>.json` in, `ads/results/<name>.json` out (same pattern as meta-ops).
- `ads/reports/<date>.md`: daily report written by the 08:00 IST cron.
- `ads/state.json`: ids, launch date, last budget shift, last creative date.
- `ads/data/leads_by_ad.json`: counts per ad id from the Leads sheet (see below). Counts only.

## Ops
| op | what | spends? |
|---|---|---|
| `check` | read-only preflight: page, WhatsApp link on the page, account, targeting resolution and audience size | no |
| `status` | campaign, ad sets, ads, spend today and this month | no |
| `setup` | creates campaign, ad sets A and B, 6 ads, all PAUSED. Idempotent | no |
| `launch` | turns everything on. Refused unless `budget_approved` and `launch_approved` are true | yes |
| `daily` | autopilot (cron runs it; `{"op":"daily","dry_run":true}` to preview) | adjusts only |
| `add_ads` | `{"op":"add_ads","adset_key":"A","ads":[{image,name,headline,text}]}`; live only if the campaign is already approved and running | within caps |
| `pause_ad` / `pause_all` | FIT campaign only | stops spend |
| `audiences` | builds TY page and Instagram engager audiences; optional `phones_sha256` list for WhatsApp chatters (hash before sending, never plain numbers: this repo is public) | no |
| `enable_retargeting` | week 2: ad set C, funded by moving budget out of A and B (total unchanged) | within caps |

## Daily rules (in code)
1. Hard caps: if month-to-date spend plus today's budget would pass `monthly_cap_inr`, pause the campaign. If ad set budgets add up to more than `daily_cap_inr`, scale them down. The campaign also has a lifetime spend cap equal to the monthly cap.
2. Pause an ad once it has spent `pause_multiple` x the target cost per qualified lead with no qualified lead. Until the Leads sheet join exists, the proxy is: no WhatsApp conversation after that spend, or cost per conversation above 3x the target.
3. From day 3 after launch, once a day, move up to 20% of the worst ad set's budget to the best (by cost per qualified lead, else per conversation over the last 3 days). Total never rises; no ad set below `min_adset_daily_inr`.
4. Flags: 7-day frequency above 3 (fatigue), and 2 fresh creatives due every 7 days.

## The daily Claude run (after launch)
1. Before 08:00 IST: read the Leads sheet (1E9HR3b-hnmlnuk6aWXnGQ-BcC6YIv13vZPASHKuRmSk) and write `ads/data/leads_by_ad.json` as `{"generated_at_epoch":..., "by_ad": {"<ad id>": {"chats":n, "qualified":n, "visit_planned":n, "visit_done":n, "booked":n}}}`. Qualified = any status past "Call them - New Lead" other than Not Interested. Needs the ad id column the bot will fill from the WhatsApp referral (pending). Without it, skip this step.
2. After 08:15 IST: read `ads/reports/<today>.md` and put 3 to 5 lines in the morning message: spend yesterday and month to date against cap, chats and cost per chat, qualified and visits, what the autopilot changed, what is due (creatives, approvals). No em dashes.
3. When creatives are due, make 2 in the FIT creative studio style (HRERA top right, "Representational model" label), add them under `ads/creatives/`, and push an `add_ads` request.

## Copy rules
FIT facts only from `website/FIT_PAGE_BRIEF.md`. No return promises, no price claims until Rishi gives an approved rate line, no ownership claim until leasehold is ruled out. No em dashes.

## Coordination with the WhatsApp autopilot (Rishi, 17 Nov 2026)
Full rules: `strategy/CHANNEL_COORDINATION.md` in the Claude Project.
- Ads money is additional. This agent never reads, lowers or reallocates the WhatsApp autopilot's budget or wallet. Moving money between channels is Rishi's call.
- One lead record (Leads sheet, keyed by phone). Ads tag `ctwa` + ad id, the autopilot tags `wa_outbound` + cell.
- Ad chatters who don't convert go to the autopilot's warm track. Autopilot cell learnings shape ad targeting and hooks.
- Excluded from ads: Not Interested, opted out, Site Visit Planned and Visit Done (config `exclude_audience_names`, refreshed daily by the Claude run with `{"op":"audiences","lists":{"<name>":[sha256,...]}}`).
- Audiences (warm-up halves per cell, unreachable, exclusions) are built by the WhatsApp Lambda straight into Meta. No phone numbers or hashes in this public repo.
- Joint wave: warm-up ads 4 days before the autopilot's first touch in a cell, reminder ads during follow-ups, 50/50 holdout per cell to measure lift.
