// One-off, 28 Nov 2026 (pf.gads): at Rishi's word (18:11, "make the ads most effective, legal fine print is not the focus")
// replace the two HRERA-number description lines in each live FIT Search ad with two selling lines for that ad group.
// "HRERA registered" stays as a short trust phrase. Only enabled ad groups in the two FIT Search campaigns.
var NEW = {
  'Haryana industrial plots': [
    'Own substation, STP, CCTV and 18 m and 24 m roads. 10 min from NH-152D.',
    'HRERA registered. Get the site plan and plot sizes on WhatsApp in minutes.'],
  'Rohtak industrial plots': [
    'Own substation, STP, CCTV and fire safety inside one gated industrial township.',
    'HRERA registered. Get the site plan and plot sizes on WhatsApp in minutes.'],
  'Factory land and MSME': [
    'Own substation, STP and 24 m roads for trucks. 10 min from NH-152D, near IMT Rohtak.',
    'HRERA registered. Get the site plan and plot sizes on WhatsApp in minutes.'],
  'Warehouse and logistics land': [
    'Rohtak to Bhiwani highway 5 min, Delhi to Hisar highway 15 min, KMP 40 min.',
    'HRERA registered. Get the site plan and plot sizes on WhatsApp in minutes.'],
  'Brand searches': [
    'Official FIT page: site plan, plot sizes and free site visits. Chat with us on WhatsApp.',
    'Own substation, STP and 18 m and 24 m roads. HRERA registered.']
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
