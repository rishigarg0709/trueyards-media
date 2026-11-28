# Google Ads scripts (TY FIT, 319-251-6966)

Owner: Paid Search and Video Media Buyer (pf.gads). These run inside Google Ads (Tools > Bulk actions > Scripts), in Google's cloud, with no keys.

- `fit-coordination.js`: daily. Follows the shared weekly plan (`perf/plan.json` `focus.districts`, `focus.avoid`, optional `google` budgets) and the Control Room People tab (leads and qualified leads per district from every channel), sets location bids on the FIT Industry campaigns (+30% focus or proven, -30% avoid until a qualified lead, 0 otherwise), applies plan budgets within hard caps, and writes yesterday's numbers to the Control Room "Google" tab plus an Activity row per change. Never enables a paused campaign.

The copy in Google Ads is the one that runs; keep this file in step when it changes.

## Contract for the planner (perf/plan.json)
```json
"focus": {"week_of": "2026-11-30", "districts": ["Rohtak", "Jhajjar"], "avoid": ["Gurugram"], "why": "..."},
"google": {"search_category_inr": 335, "search_brand_inr": 85, "youtube_inr": 340}
```
District names as Google lists them: Rohtak, Jhajjar, Bhiwani, Sonipat, Panipat, Hisar, Jind, Gurugram, Faridabad, Rewari, Noida, Ghaziabad, North West Delhi, West Delhi, South Delhi, South West Delhi.
