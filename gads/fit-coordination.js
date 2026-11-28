/**
 * FIT coordination script for Google Ads (TY FIT, 319-251-6966).
 * Owner: Paid Search and Video Media Buyer (pf.gads). Runs daily inside Google Ads (Tools > Scripts), no keys.
 *
 * What it does, every run:
 *  1. Reads the shared weekly plan (perf/plan.json in trueyards-media, public, counts only). If the planner has
 *     written `focus.districts` / `focus.avoid`, those win; otherwise the defaults below are used.
 *  2. Reads the Control Room People tab (same Google account) and counts, per district, the FIT leads and
 *     qualified leads of the last 30 days from EVERY channel (WhatsApp autopilot, broadcasts, Meta ads, Google, inbound).
 *  3. On every "FIT Industry -" campaign (Search and YouTube) sets location bids:
 *       +30% on this week's focus districts and on any district that produced a qualified lead,
 *       -30% on "avoid" districts until they produce a qualified lead (then the cut is lifted by itself),
 *        0% everywhere else.
 *     Google ignores these under Maximise conversions / target CPA; the script then only reports.
 *  4. If the plan carries a `google` block with daily budgets, applies them within the hard caps below.
 *  5. Writes yesterday's numbers per campaign to the Control Room "Google" tab and one Activity row per change.
 *
 * It never enables a paused campaign, never creates or removes ads, and never touches Meta or WhatsApp.
 */

var CFG = {
  DRY_RUN: false,
  PLAN_URL: 'https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/perf/plan.json',
  CONTROL_ROOM_ID: '1VJ0fmL-aq-UJno2_EeB2IwWz--awbRrdXSQFFDi2JoA',
  CAMPAIGN_PREFIX: 'FIT ',            // FIT Industry - ... and FIT Brand - ...
  BID_CAMPAIGN_PREFIX: 'FIT Industry',// location bids only on the category campaigns (brand searches stay neutral)
  BOOST: 1.30,
  CUT: 0.70,
  LOOKBACK_DAYS: 30,
  // Used until the planner writes focus into perf/plan.json (GOOGLE_ADS_ROLLOUT_28NOV.md, week of 30 Nov).
  DEFAULT_FOCUS: ['Rohtak', 'Jhajjar', 'Bhiwani', 'Sonipat', 'Panipat', 'Hisar', 'Jind'],
  DEFAULT_AVOID: ['Gurugram', 'Noida', 'South Delhi', 'West Delhi'],
  // Budget guard rails (INR a day, before GST). The plan can move money only inside these.
  BUDGET_MIN: 50,
  BUDGET_MAX: { 'FIT Industry - Google Search': 600, 'FIT Brand - Google Search': 150, 'FIT Industry - YouTube': 500 },
  QUALIFIED_STAGES: ['sv', 'vd', 'vdi', 'vdn', 'booked', 'won', 'qual'],
  AGENT_ID: 'pf.gads',
  AGENT: 'Paid Search and Video Media Buyer'
};

// Town in the shared record -> district name as Google lists it in our targeting.
var TOWN_TO_DISTRICT = {
  'rohtak': 'Rohtak', 'kalanaur': 'Rohtak', 'lakhan majra': 'Rohtak', 'meham': 'Rohtak', 'sampla': 'Rohtak', 'imt rohtak': 'Rohtak',
  'bahadurgarh': 'Jhajjar', 'jhajjar': 'Jhajjar', 'beri': 'Jhajjar', 'asaudha': 'Jhajjar',
  'sonipat': 'Sonipat', 'sonepat': 'Sonipat', 'kundli': 'Sonipat', 'rai': 'Sonipat', 'gohana': 'Sonipat', 'kharkhoda': 'Sonipat', 'murthal': 'Sonipat',
  'panipat': 'Panipat', 'samalkha': 'Panipat',
  'bhiwani': 'Bhiwani', 'tosham': 'Bhiwani', 'loharu': 'Bhiwani',
  'charkhi dadri': 'Charkhi Dadri', 'dadri': 'Charkhi Dadri',
  'hisar': 'Hisar', 'hissar': 'Hisar', 'hansi': 'Hisar',
  'jind': 'Jind', 'julana': 'Jind', 'narwana': 'Jind', 'safidon': 'Jind',
  'gurugram': 'Gurugram', 'gurgaon': 'Gurugram', 'manesar': 'Gurugram', 'sohna': 'Gurugram',
  'faridabad': 'Faridabad', 'ballabgarh': 'Faridabad',
  'rewari': 'Rewari', 'dharuhera': 'Rewari', 'bawal': 'Rewari',
  'noida': 'Noida', 'greater noida': 'Noida', 'ghaziabad': 'Ghaziabad',
  'bawana': 'North West Delhi', 'narela': 'North West Delhi', 'rohini': 'North West Delhi', 'pitampura': 'North West Delhi', 'alipur': 'North West Delhi',
  'mundka': 'West Delhi', 'nangloi': 'West Delhi', 'punjabi bagh': 'West Delhi', 'rajouri garden': 'West Delhi', 'kirti nagar': 'West Delhi', 'mayapuri': 'West Delhi',
  'najafgarh': 'South West Delhi', 'dwarka': 'South West Delhi',
  'okhla': 'South Delhi', 'saket': 'South Delhi', 'mehrauli': 'South Delhi'
};

function main() {
  var log = [];
  var plan = readPlan(log);
  var focus = (plan && plan.focus && plan.focus.districts && plan.focus.districts.length) ? plan.focus.districts : CFG.DEFAULT_FOCUS;
  var avoid = (plan && plan.focus && plan.focus.avoid) ? plan.focus.avoid : CFG.DEFAULT_AVOID;
  var focusSource = (plan && plan.focus && plan.focus.districts) ? 'perf/plan.json' : 'default list';

  var ss = openControlRoom(log);
  var ev = ss ? districtEvidence(ss, log) : {};
  var proven = Object.keys(ev).filter(function (d) { return ev[d].qualified > 0; });

  var changes = [];
  var camps = fitCampaigns();
  camps.forEach(function (c) {
    if (c.targeting && c.getName().indexOf(CFG.BID_CAMPAIGN_PREFIX) === 0) changes = changes.concat(setLocationBids(c, focus, avoid, proven));
  });
  if (plan && plan.google) changes = changes.concat(applyBudgets(camps, plan.google));

  if (ss) {
    writeDaily(ss, camps);
    writeActivity(ss, changes, focusSource, focus, proven);
  }
  Logger.log('Focus (' + focusSource + '): ' + focus.join(', '));
  Logger.log('Districts with a qualified lead in ' + CFG.LOOKBACK_DAYS + ' days: ' + (proven.join(', ') || 'none'));
  Logger.log('Evidence: ' + JSON.stringify(ev));
  Logger.log('Changes: ' + (changes.length ? changes.join(' | ') : 'none'));
  log.forEach(function (l) { Logger.log(l); });
}

function readPlan(log) {
  try {
    return JSON.parse(UrlFetchApp.fetch(CFG.PLAN_URL, { muteHttpExceptions: true }).getContentText());
  } catch (e) { log.push('Plan not read: ' + e); return null; }
}

function openControlRoom(log) {
  try { return SpreadsheetApp.openById(CFG.CONTROL_ROOM_ID); }
  catch (e) { log.push('Control Room not reachable from this Google account: ' + e); return null; }
}

// Leads and qualified leads per district over the lookback, from every channel in the shared record.
function districtEvidence(ss, log) {
  var sh = ss.getSheetByName('People');
  if (!sh) { log.push('People tab missing'); return {}; }
  var v = sh.getDataRange().getValues();
  var h = v[0], iTown = h.indexOf('town'), iLead = h.indexOf('lead_at'), iStage = h.indexOf('stage'), iSrc = h.indexOf('source');
  var since = new Date(Date.now() - CFG.LOOKBACK_DAYS * 864e5);
  var out = {}, seen = { rows: v.length - 1, leads: 0, unmapped: {} };
  for (var r = 1; r < v.length; r++) {
    var town = String(v[r][iTown] || '').trim().toLowerCase();
    var raw = v[r][iLead];
    if (raw) seen.leads++;
    var d = TOWN_TO_DISTRICT[town];
    if (town && !d) seen.unmapped[town] = (seen.unmapped[town] || 0) + 1;
    if (!d || !raw) continue;
    var t = raw instanceof Date ? raw : new Date(String(raw).trim().replace(' ', 'T') + (String(raw).length <= 16 ? ':00' : '') + '+05:30');
    if (isNaN(t) || t < since) continue;
    var e = out[d] || (out[d] = { leads: 0, qualified: 0, bySource: {} });
    e.leads++;
    if (CFG.QUALIFIED_STAGES.indexOf(String(v[r][iStage] || '').toLowerCase()) >= 0) e.qualified++;
    var s = String(v[r][iSrc] || 'other');
    e.bySource[s] = (e.bySource[s] || 0) + 1;
  }
  log.push('People rows ' + seen.rows + ', with a lead date ' + seen.leads + '; towns not mapped to a district: ' + JSON.stringify(seen.unmapped));
  return out;
}

function fitCampaigns() {
  var list = [];
  [AdsApp.campaigns(), AdsApp.videoCampaigns()].forEach(function (sel) {
    var it = sel.withCondition("Name STARTS_WITH '" + CFG.CAMPAIGN_PREFIX + "'").withCondition("Status != REMOVED").get();
    while (it.hasNext()) list.push(it.next());
  });
  return list.concat(demandGenCampaigns());
}

// Demand Gen campaigns (FIT Industry - YouTube) are not in AdsApp.campaigns() or videoCampaigns(), so read them with
// GAQL and wrap them in the few methods this script uses (name, status, budget, yesterday's stats, bidding).
// They target states, not districts, so they get no location bids (no targeting()).
function demandGenCampaigns() {
  var out = [];
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
  var it = AdsApp.search("SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.resource_name, " +
    "campaign_budget.amount_micros FROM campaign WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND campaign.status != 'REMOVED' " +
    "AND campaign.name LIKE '" + CFG.CAMPAIGN_PREFIX + "%'");
  while (it.hasNext()) {
    (function (r) {
      var id = r.campaign.id, budgetRn = r.campaignBudget.resourceName, amount = Number(r.campaignBudget.amountMicros) / 1e6;
      out.push({
        getName: function () { return r.campaign.name; },
        isEnabled: function () { return r.campaign.status === 'ENABLED'; },
        getBiddingStrategyType: function () { return r.campaign.biddingStrategyType; },
        getBudget: function () {
          return {
            getAmount: function () { return amount; },
            setAmount: function (v) {
              AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: budgetRn, amountMicros: Math.round(v * 1e6) }, updateMask: 'amount_micros' } });
              amount = v;
            }
          };
        },
        getStatsFor: function () {
          var m = { cost: 0, impressions: 0, clicks: 0, conversions: 0 };
          var s = AdsApp.search("SELECT metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions FROM campaign WHERE campaign.id = " + id + " AND segments.date DURING YESTERDAY");
          if (s.hasNext()) { var x = s.next().metrics; m = { cost: Number(x.costMicros || 0) / 1e6, impressions: Number(x.impressions || 0), clicks: Number(x.clicks || 0), conversions: Number(x.conversions || 0) }; }
          return { getCost: function () { return m.cost; }, getImpressions: function () { return m.impressions; }, getClicks: function () { return m.clicks; }, getConversions: function () { return m.conversions; } };
        }
      });
    })(it.next());
  }
  return out;
}

function baseName(loc) { return String(loc.getName()).split(',')[0].trim(); }

function setLocationBids(c, focus, avoid, proven) {
  var out = [];
  var smart = /TARGET_CPA|MAXIMIZE_CONVERSIONS|TARGET_ROAS|MAXIMIZE_CONVERSION_VALUE/.test(String(c.getBiddingStrategyType ? c.getBiddingStrategyType() : ''));
  var it = c.targeting().targetedLocations().get();
  while (it.hasNext()) {
    var loc = it.next();
    var n = baseName(loc);
    var want = 1.0;
    if (focus.indexOf(n) >= 0 || proven.indexOf(n) >= 0) want = CFG.BOOST;
    else if (avoid.indexOf(n) >= 0) want = CFG.CUT;
    var cur = loc.getBidModifier();
    if (Math.abs(cur - want) > 0.001) {
      if (!CFG.DRY_RUN) loc.setBidModifier(want);
      out.push(c.getName() + ': ' + loc.getName() + ' ' + pct(cur) + ' to ' + pct(want) + (smart ? ' (kept for reporting; smart bidding ignores it)' : ''));
    }
  }
  return out;
}

function applyBudgets(camps, g) {
  var out = [];
  var want = {
    'FIT Industry - Google Search': g.search_category_inr,
    'FIT Brand - Google Search': g.search_brand_inr,
    'FIT Industry - YouTube': g.youtube_inr
  };
  camps.forEach(function (c) {
    var w = want[c.getName()];
    if (w === undefined || w === null) return;
    var cap = CFG.BUDGET_MAX[c.getName()] || CFG.BUDGET_MIN;
    w = Math.max(CFG.BUDGET_MIN, Math.min(cap, Math.round(Number(w))));
    var b = c.getBudget(), cur = b.getAmount();
    if (Math.abs(cur - w) >= 1) {
      if (!CFG.DRY_RUN) b.setAmount(w);
      out.push(c.getName() + ': budget INR ' + cur + ' to ' + w + ' a day (plan)');
    }
  });
  return out;
}

function writeDaily(ss, camps) {
  var sh = ss.getSheetByName('Google') || ss.insertSheet('Google');
  if (sh.getLastRow() === 0) sh.appendRow(['date', 'campaign', 'status', 'budget_inr', 'spend_inr', 'impressions', 'clicks', 'conversions', 'bidding', 'written_at']);
  var day = Utilities.formatDate(new Date(Date.now() - 864e5), 'Asia/Kolkata', 'yyyy-MM-dd');
  var now = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd HH:mm');
  camps.forEach(function (c) {
    var s = c.getStatsFor('YESTERDAY');
    sh.appendRow([day, c.getName(), c.isEnabled() ? 'ENABLED' : 'PAUSED', c.getBudget().getAmount(), round2(s.getCost()), s.getImpressions(), s.getClicks(),
      round2(s.getConversions ? s.getConversions() : 0), String(c.getBiddingStrategyType ? c.getBiddingStrategyType() : ''), now]);
  });
}

function writeActivity(ss, changes, focusSource, focus, proven) {
  if (!changes.length) return;
  var sh = ss.getSheetByName('Activity');
  if (!sh) return;
  var now = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd HH:mm');
  var detail = (CFG.DRY_RUN ? 'Dry run, would change: ' : 'FIT coordination script: ') + changes.length + ' location bid or budget changes (focus from ' + focusSource + ': ' +
    focus.join(', ') + '; qualified leads in ' + (proven.join(', ') || 'no district') + '). ' + changes.slice(0, 6).join('; ') + (changes.length > 6 ? '; ...' : '');
  sh.appendRow([now, CFG.AGENT_ID, CFG.AGENT, 'auto', detail.slice(0, 900), 'Google Ads TY FIT 319-251-6966']);
}

function pct(m) { var p = Math.round((m - 1) * 100); return (p > 0 ? '+' : '') + p + '%'; }
function round2(x) { return Math.round(Number(x || 0) * 100) / 100; }
