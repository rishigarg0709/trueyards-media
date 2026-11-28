/**
 * SMX Google data (GA4 + Search Console), owner Paid Search and Video Media Buyer (pf.gads). Added 28 Nov 2026.
 * Runs every 15 minutes in Google's cloud (Apps Script, Rishi's Google sign-in, no keys).
 *  - Works through Control Room "GoogleOps" rows whose op starts with "ga4." or "gsc." and writes the result on the row.
 *  - Once an hour refreshes tabs GA4_Daily, GA4_Sources, GA4_Pages, GSC_Queries, GSC_Pages.
 * Install once: run setup() and click Allow. setup() also prints which GA4 property and Search Console site it picked.
 * ops: ga4.report{dimensions[],metrics[],start,end,limit}  ga4.keyevent{eventName}  ga4.keyevents
 *      gsc.query{dimensions[],start,end,rowLimit}  gsc.inspect{url}  gsc.sitemap{url}  gsc.sitemaps
 */
var CR = '1VJ0fmL-aq-UJno2_EeB2IwWz--awbRrdXSQFFDi2JoA';
var TZ = 'Asia/Kolkata';
var AGENT_ID = 'pf.gads', AGENT = 'Paid Search and Video Media Buyer';

function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('run').timeBased().everyMinutes(15).create();
  PropertiesService.getScriptProperties().deleteAllProperties();
  Logger.log('GA4 property: ' + ga4Property() + ' | Search Console site: ' + gscSite());
  run(true);
}

function run(force) {
  var ss = SpreadsheetApp.openById(CR);
  processQueue(ss);
  var p = PropertiesService.getScriptProperties(), last = Number(p.getProperty('lastData') || 0);
  if (force === true || Date.now() - last > 55 * 60e3) {
    try { writeData(ss); p.setProperty('lastData', String(Date.now())); } catch (e) { Logger.log('data: ' + e); }
  }
}

// ---------------------------------------------------------------- APIs
function api(method, url, body) {
  var o = { method: method, headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() }, muteHttpExceptions: true };
  if (body) { o.contentType = 'application/json'; o.payload = JSON.stringify(body); }
  var r = UrlFetchApp.fetch(url, o), t = r.getContentText(), j = t ? JSON.parse(t) : {};
  if (r.getResponseCode() >= 300) throw new Error(r.getResponseCode() + ' ' + (j.error ? j.error.message : t).slice(0, 500));
  return j;
}

function ga4Property() {
  var p = PropertiesService.getScriptProperties(), v = p.getProperty('ga4');
  if (v) return v;
  var list = [];
  (api('get', 'https://analyticsadmin.googleapis.com/v1beta/accountSummaries?pageSize=200').accountSummaries || []).forEach(function (a) {
    (a.propertySummaries || []).forEach(function (s) { list.push(s); });
  });
  if (!list.length) throw new Error('this Google account sees no GA4 property');
  var pick = list.filter(function (s) { return /true\s*yards/i.test(s.displayName); })[0] || list[0];
  p.setProperty('ga4', pick.property);
  return pick.property;
}

function gscSite() {
  var p = PropertiesService.getScriptProperties(), v = p.getProperty('gsc');
  if (v) return v;
  var sites = (api('get', 'https://www.googleapis.com/webmasters/v3/sites').siteEntry || []).filter(function (s) {
    return /trueyards\.in/.test(s.siteUrl) && s.permissionLevel !== 'siteUnverifiedUser';
  });
  if (!sites.length) throw new Error('this Google account has no verified Search Console site for trueyards.in');
  var pick = sites.filter(function (s) { return /^sc-domain:/.test(s.siteUrl); })[0] || sites[0];
  p.setProperty('gsc', pick.siteUrl);
  return pick.siteUrl;
}

function ga4Run(dims, mets, start, end, limit) {
  var j = api('post', 'https://analyticsdata.googleapis.com/v1beta/' + ga4Property() + ':runReport', {
    dateRanges: [{ startDate: start || '28daysAgo', endDate: end || 'today' }],
    dimensions: (dims || []).map(function (d) { return { name: d }; }),
    metrics: (mets || ['sessions']).map(function (m) { return { name: m }; }),
    limit: limit || 1000
  });
  return (j.rows || []).map(function (r) {
    return (r.dimensionValues || []).map(function (d) { return d.value; }).concat((r.metricValues || []).map(function (m) { return Number(m.value); }));
  });
}

function gscRun(dims, start, end, rowLimit) {
  var j = api('post', 'https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(gscSite()) + '/searchAnalytics/query', {
    startDate: start || day(-30), endDate: end || day(-2), dimensions: dims || ['query'], rowLimit: rowLimit || 1000
  });
  return (j.rows || []).map(function (r) {
    return (r.keys || []).concat([r.clicks, r.impressions, Math.round(r.ctr * 10000) / 100, Math.round(r.position * 10) / 10]);
  });
}

// ---------------------------------------------------------------- queue
function processQueue(ss) {
  var sh = ss.getSheetByName('GoogleOps');
  if (!sh) return;
  var v = sh.getDataRange().getValues(), h = v[0], c = {};
  ['id', 'by', 'op', 'args', 'status', 'result', 'done_at'].forEach(function (k) { c[k] = h.indexOf(k); });
  for (var r = 1; r < v.length; r++) {
    var op = String(v[r][c.op] || '').trim(), st = String(v[r][c.status] || '').trim().toLowerCase();
    if (!/^(ga4|gsc)\./.test(op) || (st && st !== 'pending')) continue;
    var ok = true, res;
    try { var a = String(v[r][c.args] || '').trim(); res = runOp(ss, op, a ? JSON.parse(a) : {}); }
    catch (e) { ok = false; res = String(e && e.message ? e.message : e); }
    var text = typeof res === 'string' ? res : JSON.stringify(res);
    sh.getRange(r + 1, c.status + 1).setValue(ok ? 'done' : 'failed');
    sh.getRange(r + 1, c.result + 1).setValue(text.slice(0, 45000));
    sh.getRange(r + 1, c.done_at + 1).setValue(Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'));
    var act = ss.getSheetByName('Activity');
    if (act) act.appendRow([Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm'), AGENT_ID, AGENT, 'googleops',
      ('for ' + (v[r][c.by] || 'unknown') + ': ' + op + (ok ? ' done' : ' failed') + ' (GoogleOps ' + v[r][c.id] + '): ' + text.slice(0, 300)).slice(0, 900), 'Control Room GoogleOps']);
  }
}

function runOp(ss, op, a) {
  switch (op) {
    case 'ga4.report':
      var rows = ga4Run(a.dimensions, a.metrics, a.start, a.end, a.limit);
      writeTable(ss, 'GA4_Query', (a.dimensions || []).concat(a.metrics || ['sessions']), rows);
      return rows.length + ' rows in tab GA4_Query; first: ' + JSON.stringify(rows.slice(0, 5));
    case 'ga4.keyevents':
      return (api('get', 'https://analyticsadmin.googleapis.com/v1beta/' + ga4Property() + '/keyEvents').keyEvents || []).map(function (k) { return k.eventName; });
    case 'ga4.keyevent':
      if (!a.eventName) throw new Error('args.eventName missing');
      return api('post', 'https://analyticsadmin.googleapis.com/v1beta/' + ga4Property() + '/keyEvents', { eventName: a.eventName, countingMethod: 'ONCE_PER_EVENT' }).name;
    case 'gsc.query':
      var g = gscRun(a.dimensions, a.start, a.end, a.rowLimit);
      writeTable(ss, 'GSC_Query', (a.dimensions || ['query']).concat(['clicks', 'impressions', 'ctr_pct', 'position']), g);
      return g.length + ' rows in tab GSC_Query; first: ' + JSON.stringify(g.slice(0, 5));
    case 'gsc.inspect':
      var i = api('post', 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', { inspectionUrl: a.url, siteUrl: gscSite() });
      var x = i.inspectionResult && i.inspectionResult.indexStatusResult || {};
      return { verdict: x.verdict, coverage: x.coverageState, lastCrawl: x.lastCrawlTime, canonical: x.googleCanonical };
    case 'gsc.sitemaps':
      return (api('get', 'https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(gscSite()) + '/sitemaps').sitemap || []).map(function (s) { return s.path + ' ' + (s.lastDownloaded || ''); });
    case 'gsc.sitemap':
      api('put', 'https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(gscSite()) + '/sitemaps/' + encodeURIComponent(a.url));
      return 'sitemap submitted: ' + a.url;
    default: throw new Error('unknown op ' + op);
  }
}

// ---------------------------------------------------------------- data tabs
function writeData(ss) {
  var stamp = Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm');
  var m = ['sessions', 'totalUsers', 'newUsers', 'engagedSessions', 'keyEvents'];
  put(ss, 'GA4_Daily', ['date'].concat(m), ga4Run(['date'], m, '30daysAgo', 'today', 100).sort().reverse(), stamp);
  put(ss, 'GA4_Sources', ['source_medium', 'campaign'].concat(m), ga4Run(['sessionSourceMedium', 'sessionCampaignName'], m, '7daysAgo', 'today', 500), stamp);
  put(ss, 'GA4_Pages', ['page', 'views', 'sessions', 'keyEvents'], ga4Run(['pagePath'], ['screenPageViews', 'sessions', 'keyEvents'], '7daysAgo', 'today', 500), stamp);
  put(ss, 'GSC_Queries', ['query', 'clicks', 'impressions', 'ctr_pct', 'position'], gscRun(['query'], day(-30), day(-2), 1000), stamp);
  put(ss, 'GSC_Pages', ['page', 'clicks', 'impressions', 'ctr_pct', 'position'], gscRun(['page'], day(-30), day(-2), 500), stamp);
}

function put(ss, name, head, rows, stamp) {
  writeTable(ss, name, head.concat(['updated_at']), rows.map(function (r) { return r.concat([stamp]); }));
}

function writeTable(ss, name, head, rows) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clearContents();
  var all = [head].concat(rows).map(function (r) { var o = r.slice(0, head.length); while (o.length < head.length) o.push(''); return o; });
  sh.getRange(1, 1, all.length, head.length).setValues(all);
}

function day(off) { return Utilities.formatDate(new Date(Date.now() + off * 864e5), TZ, 'yyyy-MM-dd'); }
