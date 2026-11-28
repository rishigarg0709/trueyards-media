/**
 * FIT coordination script for Google Ads (TY FIT, 319-251-6966).
 * Owner: Paid Search and Video Media Buyer (pf.gads). Runs inside Google Ads (Tools > Scripts), no keys.
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

function coordinationMain() {
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
    if (c.getName().indexOf(CFG.BID_CAMPAIGN_PREFIX) === 0) changes = changes.concat(setLocationBids(c, focus, avoid, proven));
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
  return list;
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

// ===================================================================================================
// SMX Google Ads ops queue (pf.gads). Added 28 Nov 2026. Same script, same Google sign-in, no keys.
//
// Runs every hour inside Google Ads (Google's cloud). Each run:
//  1. Works through new rows of the Control Room tab "GoogleOps" (requests from any agent, written with
//     the Google Sheets connector) and writes status, result and done_at back on the same row.
//  2. Refreshes the data tabs G_Campaigns, G_Ads, G_Keywords, G_SearchTerms (overwritten every hour).
//  3. In the 08:00 IST hour (or on op "coordination") runs the daily FIT coordination above.
// Rows whose op starts with "ga4." or "gsc." belong to the Apps Script "SMX Google data" and are skipped.
//
// Request row: id | requested_at | by (role id) | op | args (JSON) | rishi_go | status | result | done_at
// rishi_go is typed by Rishi only. It is needed to enable anything paused or to raise a budget.
// ===================================================================================================

var OPS = {
  TAB: 'GoogleOps',
  HEAD: ['id', 'requested_at', 'by', 'op', 'args', 'rishi_go', 'status', 'result', 'done_at'],
  MAX_PER_RUN: 25,
  COORD_HOUR: 8,
  TZ: 'Asia/Kolkata',
  CUSTOMER: '3192516966'
};

function main() {
  var ss = SpreadsheetApp.openById(CFG.CONTROL_ROOM_ID);
  var state = { coordination: false };
  processQueue(ss, state);
  var hour = Number(Utilities.formatDate(new Date(), OPS.TZ, 'H'));
  if (hour === OPS.COORD_HOUR || state.coordination) coordinationMain();
  try { writeData(ss); } catch (e) { Logger.log('Data tabs not written: ' + e); }
}

// ---------------------------------------------------------------- queue
function processQueue(ss, state) {
  var sh = ss.getSheetByName(OPS.TAB);
  if (!sh) { sh = ss.insertSheet(OPS.TAB); sh.appendRow(OPS.HEAD); return; }
  var v = sh.getDataRange().getValues();
  if (v.length < 2) return;
  var h = v[0], col = {};
  OPS.HEAD.forEach(function (k) { col[k] = h.indexOf(k); });
  var done = 0;
  for (var r = 1; r < v.length && done < OPS.MAX_PER_RUN; r++) {
    var op = String(v[r][col.op] || '').trim();
    var status = String(v[r][col.status] || '').trim().toLowerCase();
    if (!op || (status && status !== 'pending')) continue;
    if (/^(ga4|gsc)\./.test(op)) continue;
    var res, ok = true;
    try {
      var args = String(v[r][col.args] || '').trim();
      args = args ? JSON.parse(args) : {};
      var go = String(v[r][col.rishi_go] || '').trim().toUpperCase() === 'GO';
      res = runOp(op, args, go, ss, state);
    } catch (e) { ok = false; res = String(e && e.message ? e.message : e); }
    var text = typeof res === 'string' ? res : JSON.stringify(res);
    sh.getRange(r + 1, col.status + 1).setValue(ok ? 'done' : 'failed');
    sh.getRange(r + 1, col.result + 1).setValue(text.slice(0, 45000));
    sh.getRange(r + 1, col.done_at + 1).setValue(Utilities.formatDate(new Date(), OPS.TZ, 'yyyy-MM-dd HH:mm'));
    activity(ss, v[r][col.by], op + ' ' + (ok ? 'done' : 'failed') + ' (GoogleOps ' + v[r][col.id] + '): ' + text.slice(0, 300));
    done++;
  }
}

function runOp(op, a, go, ss, state) {
  switch (op) {
    case 'help':
      return 'ops: help, report, coordination, query{gaql,tab?}, pause{campaign,adGroup?}, enable{campaign,adGroup?}+GO, ' +
        'budget{campaign,inr} (raise needs GO), negatives{campaign,keywords[]}, keywords{campaign,adGroup,keywords[]}, ' +
        'keyword.pause{campaign,adGroup,text}, mutate{operations[]} (enable or budget ops need GO)';
    case 'report': return 'data tabs refresh at the end of this run';
    case 'coordination': state.coordination = true; return 'daily coordination runs at the end of this run';
    case 'query': return opQuery(ss, a);
    case 'pause': return setStatus(a, false);
    case 'enable':
      if (!go) throw new Error('enable needs rishi_go = GO');
      return setStatus(a, true);
    case 'budget': return opBudget(a, go);
    case 'negatives': return opNegatives(a);
    case 'keywords': return opKeywords(a);
    case 'keyword.pause': return opKeywordPause(a);
    case 'mutate': return opMutate(a, go);
    default: throw new Error('unknown op ' + op + ' (try help)');
  }
}

function findCampaign(name) {
  if (!name) throw new Error('args.campaign missing');
  var sels = [AdsApp.campaigns(), AdsApp.videoCampaigns(), AdsApp.performanceMaxCampaigns()];
  for (var i = 0; i < sels.length; i++) {
    var it = sels[i].withCondition("Name = '" + String(name).replace(/'/g, "\\'") + "'").get();
    if (it.hasNext()) return it.next();
  }
  throw new Error('campaign not found: ' + name);
}

function findAdGroup(c, name) {
  var it = c.adGroups().withCondition("Name = '" + String(name).replace(/'/g, "\\'") + "'").get();
  if (!it.hasNext()) throw new Error('ad group not found: ' + name);
  return it.next();
}

function setStatus(a, on) {
  var c = findCampaign(a.campaign), t = a.adGroup ? findAdGroup(c, a.adGroup) : c;
  if (on) t.enable(); else t.pause();
  return (a.adGroup ? 'ad group ' + a.adGroup + ' in ' : 'campaign ') + a.campaign + (on ? ' enabled' : ' paused');
}

function opBudget(a, go) {
  var c = findCampaign(a.campaign), b = c.getBudget(), cur = b.getAmount();
  var w = Math.round(Number(a.inr));
  if (!(w >= CFG.BUDGET_MIN)) throw new Error('inr must be at least ' + CFG.BUDGET_MIN);
  var cap = CFG.BUDGET_MAX[c.getName()];
  if (cap && w > cap) throw new Error('above the hard cap INR ' + cap + ' a day for this campaign');
  if (w > cur && !go) throw new Error('raising a budget needs rishi_go = GO');
  b.setAmount(w);
  return a.campaign + ': budget INR ' + cur + ' to ' + w + ' a day';
}

function opNegatives(a) {
  var c = findCampaign(a.campaign), n = 0;
  (a.keywords || []).forEach(function (k) { c.createNegativeKeyword(String(k)); n++; });
  return n + ' negative keywords added to ' + a.campaign;
}

function opKeywords(a) {
  var g = findAdGroup(findCampaign(a.campaign), a.adGroup), out = [];
  (a.keywords || []).forEach(function (k) {
    var r = g.newKeywordBuilder().withText(String(k)).build();
    out.push(k + (r.isSuccessful() ? ' ok' : ' failed: ' + r.getErrors().join('; ')));
  });
  return out.join(' | ');
}

function opKeywordPause(a) {
  var g = findAdGroup(findCampaign(a.campaign), a.adGroup);
  var it = g.keywords().withCondition("Text = '" + String(a.text).replace(/'/g, "\\'") + "'").get(), n = 0;
  while (it.hasNext()) { it.next().pause(); n++; }
  return n + ' keywords paused';
}

function opMutate(a, go) {
  var ops = a.operations || [];
  if (!ops.length) throw new Error('args.operations is empty');
  var s = JSON.stringify(ops);
  var risky = /"campaignBudgetOperation"/.test(s) || /"status"\s*:\s*"ENABLED"/.test(s);
  if (risky && !go) throw new Error('enabling or budget operations need rishi_go = GO');
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  return res.map(function (r) {
    return r.isSuccessful() ? 'ok ' + r.getResourceName() : 'failed ' + r.getErrorMessages().join('; ');
  });
}

function opQuery(ss, a) {
  if (!a.gaql) throw new Error('args.gaql missing');
  var it = AdsApp.search(a.gaql), rows = [], keys = {};
  while (it.hasNext() && rows.length < (a.max || 5000)) {
    var f = flat(it.next(), '', {});
    Object.keys(f).forEach(function (k) { keys[k] = 1; });
    rows.push(f);
  }
  var head = Object.keys(keys);
  var tab = a.tab && /^G_Query/.test(a.tab) ? a.tab : 'G_Query';
  writeTable(ss, tab, head, rows.map(function (f) { return head.map(function (k) { return f[k] === undefined ? '' : f[k]; }); }));
  return rows.length + ' rows written to tab ' + tab + (rows.length ? '; first: ' + JSON.stringify(rows[0]).slice(0, 1500) : '');
}

function flat(o, p, out) {
  Object.keys(o).forEach(function (k) {
    var v = o[k], key = p ? p + '.' + k : k;
    if (v && typeof v === 'object' && !Array.isArray(v)) flat(v, key, out);
    else out[key] = Array.isArray(v) ? JSON.stringify(v) : v;
  });
  return out;
}

function activity(ss, by, detail) {
  var sh = ss.getSheetByName('Activity');
  if (!sh) return;
  sh.appendRow([Utilities.formatDate(new Date(), OPS.TZ, 'yyyy-MM-dd HH:mm'), CFG.AGENT_ID, CFG.AGENT, 'googleops',
    ('for ' + (by || 'unknown') + ': ' + detail).slice(0, 900), 'Control Room GoogleOps']);
}

// ---------------------------------------------------------------- data tabs
function writeData(ss) {
  var stamp = Utilities.formatDate(new Date(), OPS.TZ, 'yyyy-MM-dd HH:mm');
  var ranges = ['TODAY', 'YESTERDAY', 'LAST_7_DAYS', 'LAST_30_DAYS'], camp = {};
  ranges.forEach(function (rg) {
    var it = AdsApp.search('SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, ' +
      'campaign_budget.amount_micros, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, ' +
      'metrics.video_views FROM campaign WHERE campaign.status != REMOVED AND segments.date DURING ' + rg);
    while (it.hasNext()) {
      var x = it.next(), id = x.campaign.id;
      var c = camp[id] || (camp[id] = { name: x.campaign.name, status: x.campaign.status, type: x.campaign.advertisingChannelType,
        budget: micros(x.campaignBudget && x.campaignBudget.amountMicros), m: {} });
      c.m[rg] = [micros(x.metrics.costMicros), num(x.metrics.impressions), num(x.metrics.clicks), num(x.metrics.conversions), num(x.metrics.videoViews)];
    }
  });
  // Campaigns with no traffic in a range do not come back for it; list them anyway.
  var all = AdsApp.search('SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign_budget.amount_micros FROM campaign WHERE campaign.status != REMOVED');
  while (all.hasNext()) {
    var y = all.next();
    if (!camp[y.campaign.id]) camp[y.campaign.id] = { name: y.campaign.name, status: y.campaign.status, type: y.campaign.advertisingChannelType,
      budget: micros(y.campaignBudget && y.campaignBudget.amountMicros), m: {} };
  }
  var head = ['campaign', 'status', 'type', 'budget_inr'];
  ranges.forEach(function (rg) { ['spend', 'impr', 'clicks', 'conv', 'views'].forEach(function (k) { head.push(rg.toLowerCase() + '_' + k); }); });
  head.push('updated_at');
  var rows = Object.keys(camp).map(function (id) {
    var c = camp[id], r = [c.name, c.status, c.type, c.budget];
    ranges.forEach(function (rg) { r = r.concat(c.m[rg] || [0, 0, 0, 0, 0]); });
    r.push(stamp);
    return r;
  });
  writeTable(ss, 'G_Campaigns', head, rows);

  table(ss, 'G_Ads', ['campaign', 'ad_group', 'ad_id', 'type', 'status', 'approval', 'ad_strength', 'final_url', 'spend_7d', 'impr_7d', 'clicks_7d', 'conv_7d', 'updated_at'],
    'SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ' +
    'ad_group_ad.ad_strength, ad_group_ad.ad.final_urls, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions ' +
    'FROM ad_group_ad WHERE ad_group_ad.status != REMOVED AND segments.date DURING LAST_7_DAYS',
    function (x) { return [x.campaign.name, x.adGroup.name, x.adGroupAd.ad.id, x.adGroupAd.ad.type, x.adGroupAd.status,
      x.adGroupAd.policySummary ? x.adGroupAd.policySummary.approvalStatus : '', x.adGroupAd.adStrength || '',
      (x.adGroupAd.ad.finalUrls || []).join(' '), micros(x.metrics.costMicros), num(x.metrics.impressions), num(x.metrics.clicks), num(x.metrics.conversions), stamp]; },
    'SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ' +
    'ad_group_ad.ad_strength, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE ad_group_ad.status != REMOVED', 3);

  table(ss, 'G_Keywords', ['campaign', 'ad_group', 'keyword', 'match', 'status', 'quality_score', 'spend_7d', 'impr_7d', 'clicks_7d', 'conv_7d', 'updated_at'],
    'SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ' +
    'ad_group_criterion.quality_info.quality_score, metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions ' +
    'FROM keyword_view WHERE ad_group_criterion.status != REMOVED AND segments.date DURING LAST_7_DAYS',
    function (x) { return [x.campaign.name, x.adGroup.name, x.adGroupCriterion.keyword.text, x.adGroupCriterion.keyword.matchType, x.adGroupCriterion.status,
      x.adGroupCriterion.qualityInfo ? (x.adGroupCriterion.qualityInfo.qualityScore || '') : '', micros(x.metrics.costMicros), num(x.metrics.impressions),
      num(x.metrics.clicks), num(x.metrics.conversions), stamp]; },
    'SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ' +
    'ad_group_criterion.quality_info.quality_score FROM keyword_view WHERE ad_group_criterion.status != REMOVED', 4);

  table(ss, 'G_SearchTerms', ['search_term', 'campaign', 'ad_group', 'term_status', 'spend_7d', 'impr_7d', 'clicks_7d', 'conv_7d', 'updated_at'],
    'SELECT search_term_view.search_term, campaign.name, ad_group.name, search_term_view.status, metrics.cost_micros, metrics.impressions, ' +
    'metrics.clicks, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_7_DAYS ORDER BY metrics.impressions DESC LIMIT 1000',
    function (x) { return [x.searchTermView.searchTerm, x.campaign.name, x.adGroup.name, x.searchTermView.status, micros(x.metrics.costMicros),
      num(x.metrics.impressions), num(x.metrics.clicks), num(x.metrics.conversions), stamp]; });
}

// Lists everything the undated query returns (zero metrics), then fills metrics from the dated query.
function table(ss, name, head, gaql, map, base, keyCols) {
  var rows = [], idx = {};
  function key(r) { return JSON.stringify(r.slice(0, keyCols || 3)); }
  if (base) {
    var b = AdsApp.search(base);
    while (b.hasNext()) {
      var x = b.next();
      x.metrics = { costMicros: 0, impressions: 0, clicks: 0, conversions: 0 };
      var r = map(x); idx[key(r)] = rows.length; rows.push(r);
    }
  }
  var it = AdsApp.search(gaql);
  while (it.hasNext()) {
    var m = map(it.next()), k = key(m);
    if (idx[k] !== undefined) rows[idx[k]] = m; else { idx[k] = rows.length; rows.push(m); }
  }
  writeTable(ss, name, head, rows);
}

function writeTable(ss, name, head, rows) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clearContents();
  var all = [head].concat(rows);
  sh.getRange(1, 1, all.length, head.length).setValues(all.map(function (r) {
    var o = r.slice(0, head.length);
    while (o.length < head.length) o.push('');
    return o;
  }));
}

function micros(x) { return Math.round(Number(x || 0) / 1e4) / 100; }
function num(x) { return Math.round(Number(x || 0) * 100) / 100; }
