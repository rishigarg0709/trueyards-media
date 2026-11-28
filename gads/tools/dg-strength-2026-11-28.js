// One-off, 28 Nov 2026 (pf.gads): lift the YouTube Demand Gen ad strength (campaign 24568159373) by filling
// long headlines and descriptions to 5 each (Google's best practice). Campaign stays paused.
var LONG = ['Industrial plots at Kalanaur, Rohtak with own substation, STP and 24 m truck roads.',
            'Book a free site visit to FIT, a 138-acre planned industrial township in Haryana.'];
var DESC = ['Rohtak to Bhiwani highway 5 min, Delhi to Hisar highway 15 min, KMP 40 min.',
            'Free site visit. Brochure and site plan on WhatsApp in minutes.'];
function main() {
  var it = AdsApp.search("SELECT ad_group_ad.ad.resource_name, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions FROM ad_group_ad WHERE campaign.id = 24568159373");
  var ops = [];
  while (it.hasNext()) {
    var a = it.next().adGroupAd.ad, v = a.demandGenVideoResponsiveAd;
    function merge(cur, add) { var t = (cur || []).map(function (x) { return x.text; }); add.forEach(function (s) { if (t.indexOf(s) < 0) t.push(s); }); return t.slice(0, 5).map(function (s) { return { text: s }; }); }
    ops.push({ adOperation: { update: { resourceName: a.resourceName, demandGenVideoResponsiveAd: { longHeadlines: merge(v.longHeadlines, LONG), descriptions: merge(v.descriptions, DESC) } },
      updateMask: 'demand_gen_video_responsive_ad.long_headlines,demand_gen_video_responsive_ad.descriptions' } });
  }
  AdsApp.mutateAll(ops, { partialFailure: true }).forEach(function (r, i) { Logger.log('DG op ' + i + ': ' + (r.isSuccessful() ? 'OK' : 'ERROR ' + r.getErrorMessages().join('; '))); });
}
