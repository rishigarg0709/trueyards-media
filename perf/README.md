# Performance department: shared memory

Written by the agents, read by every agent and every Claude run. Aggregates only, never phone numbers (this repo is public).

- `plan.json`: this week's split of Rishi's total (media planner, Mondays 06:30 IST). The WhatsApp Lambda reads `wa_budget_inr` at 07:30 (clamped to its own PERF_WA_MIN..PERF_WA_MAX); the ads agent reads `meta_tactics` every morning.
- `ledger.jsonl`: one line per weekly plan with the evidence behind it.
- `LEARNINGS.md`: plain-English state of what works (cost per visit by channel, warm-up lift by zone and industry, best WhatsApp cells).
- `creatives.json`: every ad's spend, results and chance of being best (creative tester). Winning angles brief the creative studio.

## The loops
1. **Inside WhatsApp** (Lambda, daily): Thompson sampling over cells, templates, slots; weekly re-score of numbers.
2. **Inside Meta** (ads agent, daily): creative tester per ad set; waste rule; 20%/day shift between prospecting ad sets.
3. **Across them** (joint waves): a cell's numbers split 50/50; ads warm one half 4 days before WhatsApp; reminders after; lift = warm vs control lead rate. Planner grows warm-up where it beats a WhatsApp lead on cost, shrinks it where it doesn't.
4. **Across channels** (planner, weekly): money moves toward the cheaper site visit, up to 20% of the total a week, with floors.
5. **Back to Meta** (CAPI): visit planned and visit done for ad-driven chats, so Meta's own optimiser learns what a good lead is.
