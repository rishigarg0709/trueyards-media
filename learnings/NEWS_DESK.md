# News desk: same-day "explained" content

Rishi asked for this on 16 Nov 2026. A scheduled run checks the news at 08:41 and 15:41 IST. When a story clears the bar, it takes over the next reel slot of the day and posts a quick take on Threads and X within the hour.

## What counts (score each 0 to 3, publish at 10+ out of 15)
1. **Affects money or rights of ordinary buyers, owners or renters** (rates, EMIs, taxes, stamp duty, circle rates, rules, court orders, big project failures).
2. **Fresh**: broke in the last 24 hours (or is trending today).
3. **India first, NCR a bonus**; global only when huge (US rate cut, China property crisis turn, a record deal).
4. **Can be explained in 45 s with one clear "what this means for you"**.
5. **Verifiable**: at least 2 reputable sources (RBI, PIB, ministries, state RERA/HRERA/UP RERA orders, Supreme Court or High Court judgments, Economic Times, Mint, Business Standard, Hindustan Times, Moneycontrol, Reuters, Bloomberg).

Watch list: RBI policy and repo rate, bank home loan rate changes, budget and income tax changes (80C, 24(b), capital gains, TDS on property), GST on property, stamp duty and circle rate revisions (Delhi, Haryana, UP, Maharashtra, Karnataka), RERA orders and big penalties, Supreme Court and High Court real estate judgments, builder insolvency (NCLT) and big project stalls, PMAY and housing schemes, big land deals and record transactions, metro and expressway approvals that move prices, quarterly housing sales reports (Anarock, Knight Frank, PropEquity), home loan and NRI rule changes.

Never: rumours, single-source scoops, stock tips, praising or attacking a named builder (report court or regulator actions factually), politics, anything about Forteasia or FIT.

## Output
- **Quick take (immediately, if the score is 12+)**: a Threads text post (under 500 chars) and an X post (under 270 chars, no links, no hashtags): what happened, the one number, what it means for a buyer. Facts only, with the source named in words ("per RBI").
- **News reel**: takes over the next unpublished reel slot today (midday if before 11:00 IST, else evening if before 17:30 IST; otherwise tomorrow's midday). Write plans/<date>/<slot>/plan.md the way the nightly prep does, marked `NEWS` at the top. Images go through the normal (same-day) image job, not the batch. Look A Newsroom Red or another news-fitting look. Hook archetype: "what changed + what it costs you". Caption names the sources and the date.
- If a nightly plan already sits in that slot, move it to plans/<date>/<slot>/displaced-plan.md and put its topic back at the top of queue/reel-topics.md as `- [ ] <topic> | displaced by news <date> | plan and images ready: plans/<date>/<slot>/displaced-plan.md` so the next nightly prep reuses it.
- **Limits**: at most 1 news reel per day and 2 quick takes per day. Never take over a slot whose reel run has already started (check log.md and meta/results for today).

## Log
Append every story considered with a score of 8+ to learnings/NEWS_LOG.md: date, headline, score, sources, action (quick take ids, slot taken, or skipped and why). Check it first so the same story is never covered twice.
