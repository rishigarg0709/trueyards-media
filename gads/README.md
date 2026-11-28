# Google Ads scripts (TY FIT, 319-251-6966)

Owner: Paid Search and Video Media Buyer (pf.gads). These run inside Google Ads (Tools > Bulk actions > Scripts), in Google's cloud, with no keys.

- `fit-ops.js` (installed in script 12795512 from 28 Nov, hourly): the cloud route for Google Ads. It is `fit-coordination.js` (renamed `coordinationMain`, still run in the 08:00 IST hour) plus an ops queue. Agents add a row to the Control Room tab `GoogleOps` with the Google Sheets connector: `id | requested_at | by | op | args (JSON) | rishi_go | status | result | done_at`. Each hourly run works through new rows and writes status, result and done_at back. Ops: `help`, `report`, `coordination`, `query {gaql, tab}` (rows to tab G_Query), `pause {campaign, adGroup}`, `enable` (needs rishi_go GO), `budget {campaign, inr}` (a raise needs GO, hard caps always), `negatives {campaign, keywords[]}`, `keywords {campaign, adGroup, keywords[]}`, `keyword.pause`, `mutate {operations[]}` (any AdsApp.mutateAll operation; enabling or budget operations need GO). Every run also overwrites the data tabs G_Campaigns (today, yesterday, 7 and 30 days), G_Ads (approval, ad strength), G_Keywords (quality score) and G_SearchTerms (7 days). Rishi alone types GO. For an answer inside the hour without waiting, anyone signed in can press Run on the script.
- `../gas/smx-google-data.gs` (Apps Script "SMX Google data", every 15 minutes): GA4 and Search Console through the same `GoogleOps` tab, ops starting `ga4.` or `gsc.`; data tabs GA4_Daily, GA4_Sources, GA4_Pages, GSC_Queries, GSC_Pages refreshed hourly.
- `fit-coordination.js`: the daily coordination part on its own (source for fit-ops.js). Follows the shared weekly plan (`perf/plan.json` `focus.districts`, `focus.avoid`, optional `google` budgets) and the Control Room People tab (leads and qualified leads per district from every channel), sets location bids on the FIT Industry campaigns (+30% focus or proven, -30% avoid until a qualified lead, 0 otherwise), applies plan budgets within hard caps, and writes yesterday's numbers to the Control Room "Google" tab plus an Activity row per change. Never enables a paused campaign.

The copy in Google Ads is the one that runs; keep this file in step when it changes.

## Contract for the planner (perf/plan.json)
```json
"focus": {"week_of": "2026-11-30", "districts": ["Rohtak", "Jhajjar"], "avoid": ["Gurugram"], "why": "..."},
"google": {"search_category_inr": 335, "search_brand_inr": 85, "youtube_inr": 340}
```
District names as Google lists them: Rohtak, Jhajjar, Bhiwani, Sonipat, Panipat, Hisar, Jind, Gurugram, Faridabad, Rewari, Noida, Ghaziabad, North West Delhi, West Delhi, South Delhi, South West Delhi.
