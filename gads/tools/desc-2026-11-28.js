// One-off, 28 Nov 2026 (pf.gads): at Rishi's word (18:11, "make the ads most effective, legal fine print is not the focus")
// replace the two HRERA-number description lines in each live FIT Search ad with two selling lines for that ad group.
// "HRERA registered" stays as a short trust phrase. Only enabled ad groups in the two FIT Search campaigns.
var NEW = {
  'Haryana industrial plots': [
    'Industrial plots from 400 to 4,000 sq yd in a planned 138-acre township near Rohtak.',
    '18 m and 24 m roads, own substation and STP. Get the site plan on WhatsApp today.'],
  'Rohtak industrial plots': [
    'Industrial plots at Kalanaur, Rohtak, 10 min from NH-152D. Get the site plan on WhatsApp.',
    'HRERA registered township with wide roads, own substation and STP. Book a site visit.'],
  'Factory land and MSME': [
    'Build your factory on a ready plot: 400 to 4,000 sq yd, wide roads, power and STP.',
    'Haryana MSME Policy 2026 benefits, subject to eligibility. Get details on WhatsApp.'],
  'Warehouse and logistics land': [
    'Truck-ready plots for warehousing: 24 m roads, 10 min from NH-152D. See the site plan.',
    'Logistics land in a planned 138-acre HRERA registered park near Rohtak. Visit today.'],
  'Brand searches': [
    'Official FIT page: site plan, plot sizes and free site visits. Chat with us on WhatsApp.',
    'Forteasia Industrial Township, Kalanaur, Rohtak. 138 acres, HRERA registered.']
};

function main() {
  Object.keys(NEW).forEach(function (g) { NEW[g].forEach(function (t) { if (t.length > 90) throw new Error('too long: ' + t); }); });
  var q = "SELECT ad_group.name, ad_group_ad.ad.resource_name, ad_group_ad.ad.responsive_search_ad.descriptions FROM ad_group_ad " +
          "WHERE campaign.id IN (24572169529, 24566018822) AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED' " +
          "AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'";
  var rows = AdsApp.search(q), ops = [], names = [];
  while (rows.hasNext()) {
    var r = rows.next(), g = r.adGroup.name, fresh = NEW[g];
    if (!fresh) { Logger.log(g + ': no new lines defined, skipped'); continue; }
    var keep = (r.adGroupAd.ad.responsiveSearchAd.descriptions || []).filter(function (d) { return d.text.indexOf('HRERA-PKL') < 0; })
      .map(function (d) { return { text: d.text }; });
    var all = keep.concat(fresh.map(function (t) { return { text: t }; })).slice(0, 4);
    ops.push({ adOperation: { update: { resourceName: r.adGroupAd.ad.resourceName, responsiveSearchAd: { descriptions: all } },
      updateMask: 'responsive_search_ad.descriptions' } });
    names.push(g + ' -> ' + all.map(function (d) { return d.text; }).join(' || '));
  }
  if (!ops.length) { Logger.log('nothing to change'); return; }
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  res.forEach(function (x, i) { Logger.log((x.isSuccessful() ? 'OK ' : 'ERROR ' + x.getErrorMessages().join('; ') + ' ') + names[i]); });
}
