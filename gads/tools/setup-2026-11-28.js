// One-off setup for TY FIT Search, 28 Nov 2026 (pf.gads), from the research audit. Campaigns stay PAUSED throughout.
// Settings, copy, keywords, negatives, assets and conversion goals. Logs every operation and its result.
var CID = '3192516966';
var IND = '24572169529', BRAND = '24566018822';
var R = function (t, id) { return 'customers/' + CID + '/' + t + '/' + id; };

var C1 = '138-acre township. HRERA-PKL-ROH-653-2025, HRERA-PKL-ROH-795-2025. www.haryanarera.gov.in';
var C2 = 'HRERA Regd: HRERA-PKL-ROH-653-2025, HRERA-PKL-ROH-795-2025. www.haryanarera.gov.in';

var ADS = {
  'Haryana industrial plots': { p2: 'Haryana-Plots',
    h: ['Industrial Plots in Haryana', 'FIT Industrial Township', '138-Acre Industrial Township', 'Plots from 400 to 4,000 Sq Yd', 'HRERA Registered Project', '18 m & 24 m Truck-Ready Roads', 'About 10 Min from NH-152D', 'Approx. 25 Min to IMT Rohtak', 'Planned Township at Kalanaur', 'Build Your Factory in Haryana', 'Industrial Land Near Rohtak', 'Ask About MSME Incentives', 'Authorised Channel Partner', 'Book a Free Site Visit', 'Get the FIT Brochure Today'],
    d: ['A 138-acre planned industrial township at Kalanaur, Rohtak. Plots of 400 to 4,000 sq yd.', 'Plan your factory or warehouse with us. Book a free site visit or get the brochure today.'],
    kw: [['industrial land haryana', 'PHRASE'], ['industrial township haryana', 'PHRASE'], ['buy industrial plot haryana', 'PHRASE'], ['industrial plots haryana', 'EXACT']] },
  'Rohtak industrial plots': { p2: 'Rohtak-Plots',
    h: ['Industrial Plots in Rohtak', 'Factory Land Near IMT Rohtak', 'FIT Kalanaur, Rohtak', 'FIT Industrial Township', '138-Acre Township in Rohtak', 'Plots from 400 to 4,000 Sq Yd', 'HRERA Registered Project', '18 m & 24 m Truck-Ready Roads', 'About 10 Min from NH-152D', 'Approx. 25 Min to IMT Rohtak', 'Your Factory Address in Rohtak', 'Visit the Site at Kalanaur', 'Authorised Channel Partner', 'Book a Free Site Visit', 'Get Plot Sizes and Site Plan'],
    d: ['Planned industrial township at Kalanaur, Rohtak, with plots from 400 to 4,000 sq yd.', 'Truck-ready 18 m and 24 m roads, near NH-152D and IMT Rohtak. Book a free site visit.'],
    kw: [['plot near imt rohtak', 'PHRASE']] },
  'Warehouse and logistics land': { p2: 'Warehouse-Land',
    h: ['Land for Warehouse in Haryana', 'Warehousing Plots Near Rohtak', 'Logistics Land Near NH-152D', 'Plots Built for Truck Movement', '18 m & 24 m Truck-Ready Roads', 'Plots from 400 to 4,000 Sq Yd', 'FIT Industrial Township', '138-Acre Industrial Township', 'HRERA Registered Project', 'About 10 Min from NH-152D', 'Approx. 25 Min to IMT Rohtak', 'Godown and Warehouse Plots', 'Authorised Channel Partner', 'Book a Free Site Visit', 'Get the FIT Brochure Today'],
    d: ['Warehouse and logistics plots of 400 to 4,000 sq yd in a 138-acre planned township.', '18 m and 24 m roads for trucks, about 10 minutes to NH-152D. Get the site plan today.'],
    kw: [['warehouse land haryana', 'PHRASE'], ['land for warehouse haryana', 'PHRASE'], ['warehousing plot', 'PHRASE'], ['logistics land haryana', 'PHRASE'], ['godown plot rohtak', 'PHRASE']] },
  'MSME policy': { rename: 'Factory land and MSME', p2: 'Factory-Land', dropKeywords: true,
    h: ['Factory Land in Haryana', 'Industrial Plots for MSMEs', 'Own the Plot for Your Factory', 'Ask About MSME Incentives', 'Guidance on Haryana Incentives', 'Plots from 400 to 4,000 Sq Yd', 'FIT Industrial Township', '138-Acre Industrial Township', 'HRERA Registered Project', '18 m & 24 m Truck-Ready Roads', 'About 10 Min from NH-152D', 'Approx. 25 Min to IMT Rohtak', 'Your Factory Address in Rohtak', 'Authorised Channel Partner', 'Book a Free Site Visit'],
    d: ['Sized for small and mid factories: plots of 400 to 4,000 sq yd at Kalanaur, Rohtak.', 'Ask our team which Haryana MSME incentives may apply to your unit. Book a site visit.'],
    kw: [['plot for factory', 'PHRASE'], ['land for factory haryana', 'PHRASE'], ['factory land rohtak', 'PHRASE'], ['msme industrial plot', 'PHRASE'], ['industrial plot for msme', 'PHRASE'], ['factory land haryana', 'PHRASE']] },
  'Brand searches': { p1: 'Forteasia', p2: 'FIT', pinH1: ['Forteasia Industrial Township', 'FIT by Forteasia Realty'],
    h: ['Forteasia Industrial Township', 'FIT by Forteasia Realty', 'FIT Kalanaur, Rohtak', 'Authorised Channel Partner', 'HRERA Registered Project', '138-Acre Industrial Township', 'Plots from 400 to 4,000 Sq Yd', 'Book a Free Site Visit', 'Get the FIT Brochure Today', 'See the Site Plan and Map', '18 m & 24 m Truck-Ready Roads', 'About 10 Min from NH-152D', 'Industrial & Commercial Plots', 'Talk to the FIT Sales Team', 'Approx. 25 Min to IMT Rohtak'],
    d: ['TrueYards is an authorised channel partner for FIT by Forteasia Realty. Visit the site.', 'A 138-acre planned industrial township at Kalanaur, Rohtak. Plots of 400 to 4,000 sq yd.'],
    kw: [] }
};

var NEG = ['rent', 'rental', 'on rent', 'for rent', 'lease deed', 'pg', 'flat', 'flats', 'apartment', '1bhk', '2bhk', '3bhk', 'villa', 'house', 'kothi', 'builder floor', 'society',
  'job', 'jobs', 'vacancy', 'recruitment', 'salary', 'career', 'internship', 'hiring',
  'tender', 'e-auction', 'auction', 'allotment', 'draw', 'lottery', 'result', 'notification', 'scheme form', 'hsiidc login', 'hsiidc e-auction', 'hsiidc allotment', 'hsvp', 'huda plot',
  'registry', 'stamp duty', 'circle rate', 'collector rate', 'jamabandi', 'khasra', 'patwari', 'court', 'case', 'dispute',
  'agriculture land', 'farm land', 'farmhouse', 'news', 'pdf', 'wikipedia', 'project report', 'how to start',
  'olx', '99acres', 'magicbricks', 'housing.com'];
var BRAND_NEG = ['gym', 'fitness', 'yoga', 'workout', 'physio', 'clothing', 'size', 'fit india'];

var SL_Q = 'utm_source=google&utm_medium=cpc&utm_campaign=fit_search_sitelink&s=';
var SITELINKS = [
  ['Book a Free Site Visit', 'Visit the township at Kalanaur', 'Our team arranges your visit', 'visit'],
  ['Get the Brochure', 'Layout, plot sizes and roads', 'Sent to you on WhatsApp', 'brochure'],
  ['View the Site Plan', 'See the 138-acre layout', 'Industrial and commercial zones', 'plan'],
  ['Location and Connectivity', 'About 10 min from NH-152D', 'Approx. 25 min to IMT Rohtak', 'location'],
  ['Plot Sizes Available', '400 to 4,000 sq yd plots', 'For factories and warehouses', 'sizes'],
  ['HRERA Registration', 'HRERA-PKL-ROH-653-2025', 'HRERA-PKL-ROH-795-2025', 'hrera'],
  ['Roads Built for Trucks', '18 m and 24 m wide roads', 'Planned for heavy vehicles', 'roads'],
  ['MSME Incentives', 'Ask about Haryana incentives', 'Our team explains the process', 'msme']];
var CALLOUTS = ['HRERA Registered', '138-Acre Township', '18 m & 24 m Wide Roads', 'Built for Truck Movement', 'Near NH-152D', 'Near IMT Rohtak', '400 to 4,000 Sq Yd Plots', 'Free Site Visit', 'Brochure on WhatsApp', 'Authorised Partner', 'Planned Industrial Zone'];
var SNIPPETS = [['Types', ['Industrial Plots', 'Warehouse Plots', 'Logistics Plots', 'Commercial Plots']],
  ['Amenities', ['18 m Wide Roads', '24 m Wide Roads', 'Planned Plot Layout', 'Truck-Ready Access']],
  ['Neighborhoods', ['Kalanaur', 'Rohtak District', 'Near NH-152D']]];
var SECONDARY_CONV = ['7841406365', '7841553490', '7841553748', '7841555407'];

function q(g) { var o = []; var it = AdsApp.search(g); while (it.hasNext()) o.push(it.next()); return o; }
function run(label, ops) {
  if (!ops.length) return [];
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var ok = 0, names = [];
  res.forEach(function (r, i) {
    if (r.isSuccessful()) { ok++; names.push(r.getResourceName()); }
    else { names.push(null); Logger.log('FAIL ' + label + ' #' + i + ': ' + r.getErrorMessages().join('; ') + ' :: ' + JSON.stringify(ops[i]).slice(0, 300)); }
  });
  Logger.log(label + ': ' + ok + ' of ' + ops.length + ' ok');
  return names;
}
function check(list, max, what) { list.forEach(function (t) { if (t.length > max) throw new Error(what + ' too long (' + t.length + '): ' + t); }); }

function main() {
  // ---- checks
  Object.keys(ADS).forEach(function (k) { var a = ADS[k]; check(a.h, 30, 'headline'); check(a.d.concat([C1, C2]), 90, 'description'); if (a.h.length !== 15) throw new Error(k + ' needs 15 headlines'); });
  SITELINKS.forEach(function (s) { check([s[0]], 25, 'sitelink'); check([s[1], s[2]], 35, 'sitelink desc'); });
  check(CALLOUTS, 25, 'callout'); SNIPPETS.forEach(function (s) { check(s[1], 25, 'snippet'); });

  // ---- 1. campaign settings
  run('campaign settings', [
    { campaignOperation: { update: { resourceName: R('campaigns', IND), targetSpend: { cpcBidCeilingMicros: 60000000 } }, updateMask: 'target_spend.cpc_bid_ceiling_micros' } },
    { campaignOperation: { update: { resourceName: R('campaigns', BRAND), targetSpend: { cpcBidCeilingMicros: 25000000 }, geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' } }, updateMask: 'target_spend.cpc_bid_ceiling_micros,geo_target_type_setting.positive_geo_target_type,geo_target_type_setting.negative_geo_target_type' } }]);
  run('auto-created assets off', [IND, BRAND].map(function (id) {
    return { campaignOperation: { update: { resourceName: R('campaigns', id), assetAutomationSettings: [{ assetAutomationType: 'TEXT_ASSET_AUTOMATION', assetAutomationStatus: 'OPTED_OUT' }] }, updateMask: 'asset_automation_settings' } };
  }));

  // ---- 2. languages English + Hindi on both
  var langOps = [];
  [IND, BRAND].forEach(function (id) { ['1000', '1023'].forEach(function (l) { langOps.push({ campaignCriterionOperation: { create: { resourceName: R('campaignCriteria', id + '~' + l), campaign: R('campaigns', id), language: { languageConstant: 'languageConstants/' + l } } } }); }); });
  run('languages', langOps);

  // ---- 3. brand locations = category locations (no bid adjustments), drop all-India
  var locs = q("SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = " + IND + " AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE")
    .map(function (r) { return r.campaignCriterion.location.geoTargetConstant; });
  var bLoc = q("SELECT campaign_criterion.resource_name, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = " + BRAND + " AND campaign_criterion.type = 'LOCATION'");
  var have = bLoc.map(function (r) { return r.campaignCriterion.location.geoTargetConstant; });
  var added = run('brand locations', locs.filter(function (g) { return have.indexOf(g) < 0; }).map(function (g) { return { campaignCriterionOperation: { create: { resourceName: R('campaignCriteria', BRAND + '~' + g.split('/')[1]), campaign: R('campaigns', BRAND), location: { geoTargetConstant: g } } } }; }));
  if (added.filter(function (x) { return x; }).length || have.length > 1) run('brand drop India', bLoc.filter(function (r) { return r.campaignCriterion.location.geoTargetConstant === 'geoTargetConstants/2356'; }).map(function (r) { return { campaignCriterionOperation: { remove: r.campaignCriterion.resourceName } }; }));

  // ---- 4. brand: "fit ..." keywords exact only; brand-only negatives
  var bk = q("SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE campaign.id = " + BRAND + " AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'");
  run('brand fit phrase removed', bk.filter(function (r) { return /^fit /.test(r.adGroupCriterion.keyword.text) && r.adGroupCriterion.keyword.matchType === 'PHRASE'; })
    .map(function (r) { return { adGroupCriterionOperation: { remove: r.adGroupCriterion.resourceName } }; }));
  run('brand negatives', BRAND_NEG.map(function (t) { return { campaignCriterionOperation: { create: { campaign: R('campaigns', BRAND), negative: true, keyword: { text: t, matchType: 'PHRASE' } } } }; }));

  // ---- 5. ad groups: rename, keywords, new RSAs, pause old RSAs
  var ags = q("SELECT ad_group.id, ad_group.name, ad_group.resource_name, campaign.id FROM ad_group WHERE campaign.id IN (" + IND + "," + BRAND + ") AND ad_group.status = 'ENABLED'");
  ags.forEach(function (r) {
    var name = r.adGroup.name, spec = ADS[name];
    if (!spec) return;
    var ag = r.adGroup.resourceName;
    var old = q("SELECT ad_group_ad.resource_name, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.path1 FROM ad_group_ad WHERE ad_group.id = " + r.adGroup.id + " AND ad_group_ad.status = 'ENABLED'");
    var finalUrls = old.length ? old[0].adGroupAd.ad.finalUrls : ['https://trueyards.in/fit'];
    if (spec.dropKeywords) {
      var ks = q("SELECT ad_group_criterion.resource_name FROM ad_group_criterion WHERE ad_group.id = " + r.adGroup.id + " AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'");
      run(name + ' old keywords removed', ks.map(function (k) { return { adGroupCriterionOperation: { remove: k.adGroupCriterion.resourceName } }; }));
    }
    run(name + ' keywords', spec.kw.map(function (k) { return { adGroupCriterionOperation: { create: { adGroup: ag, status: 'ENABLED', keyword: { text: k[0], matchType: k[1] } } } }; }));
    var heads = spec.h.map(function (t) { return (spec.pinH1 && spec.pinH1.indexOf(t) >= 0) ? { text: t, pinnedField: 'HEADLINE_1' } : { text: t }; });
    var descs = [{ text: C1, pinnedField: 'DESCRIPTION_1' }, { text: C2, pinnedField: 'DESCRIPTION_1' }, { text: spec.d[0] }, { text: spec.d[1] }];
    var made = run(name + ' new RSA', [{ adGroupAdOperation: { create: { adGroup: ag, status: 'ENABLED', ad: { finalUrls: finalUrls, responsiveSearchAd: { headlines: heads, descriptions: descs, path1: spec.p1 || 'FIT', path2: spec.p2 } } } } }]);
    if (made[0]) run(name + ' old RSA paused', old.map(function (o) { return { adGroupAdOperation: { update: { resourceName: o.adGroupAd.resourceName, status: 'PAUSED' }, updateMask: 'status' } }; }));
    if (spec.rename) run(name + ' renamed', [{ adGroupOperation: { update: { resourceName: ag, name: spec.rename }, updateMask: 'name' } }]);
    Logger.log(name + ' final URL kept: ' + JSON.stringify(finalUrls).replace(/\?.*$/, '?...'));
  });

  // ---- 6. shared negative list on both campaigns
  var ss = q("SELECT shared_set.resource_name FROM shared_set WHERE shared_set.name = 'FIT negatives' AND shared_set.status = 'ENABLED'");
  var setName = ss.length ? ss[0].sharedSet.resourceName : run('shared set', [{ sharedSetOperation: { create: { name: 'FIT negatives', type: 'NEGATIVE_KEYWORDS' } } }])[0];
  if (setName) {
    run('shared negatives', NEG.map(function (t) { return { sharedCriterionOperation: { create: { sharedSet: setName, keyword: { text: t, matchType: 'PHRASE' } } } }; }));
    run('attach negatives', [IND, BRAND].map(function (id) { return { campaignSharedSetOperation: { create: { campaign: R('campaigns', id), sharedSet: setName } } }; }));
  }

  // ---- 7. assets at account level (sitelinks, callouts, structured snippets)
  var aOps = [];
  SITELINKS.forEach(function (s) { aOps.push({ assetOperation: { create: { finalUrls: ['https://trueyards.in/fit?' + SL_Q + s[3]], sitelinkAsset: { linkText: s[0], description1: s[1], description2: s[2] } } } }); });
  CALLOUTS.forEach(function (c) { aOps.push({ assetOperation: { create: { calloutAsset: { calloutText: c } } } }); });
  SNIPPETS.forEach(function (s) { aOps.push({ assetOperation: { create: { structuredSnippetAsset: { header: s[0], values: s[1] } } } }); });
  var assets = run('assets created', aOps);
  var link = [];
  assets.forEach(function (rn, i) {
    if (!rn) return;
    var ft = i < SITELINKS.length ? 'SITELINK' : (i < SITELINKS.length + CALLOUTS.length ? 'CALLOUT' : 'STRUCTURED_SNIPPET');
    [IND, BRAND].forEach(function (id) { link.push({ campaignAssetOperation: { create: { campaign: R('campaigns', id), asset: rn, fieldType: ft } } }); });
  });
  run('assets linked to both campaigns', link);

  // ---- 8. old, unused conversion actions to secondary (the FIT offline stages stay primary)
  run('conversions secondary', SECONDARY_CONV.map(function (id) { return { conversionActionOperation: { update: { resourceName: R('conversionActions', id), primaryForGoal: false }, updateMask: 'primary_for_goal' } }; }));

  Logger.log('Setup finished.');
}
