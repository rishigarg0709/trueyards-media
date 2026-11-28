// One-off, 28 Nov 2026 (pf.gads): at Rishi's word (16:51) unpin the HRERA description lines in the
// enabled FIT Search ads, so Google can rotate all 4 descriptions and ad strength can rise.
// The HRERA text stays in the ads (unpinned), and in the callouts and the HRERA sitelink. Headline pins untouched.
var CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');

function main() {
  var q = "SELECT ad_group_ad.ad.id, ad_group_ad.ad.resource_name, ad_group.name, ad_group_ad.ad.responsive_search_ad.descriptions " +
          "FROM ad_group_ad WHERE campaign.id IN (24572169529, 24566018822) AND ad_group_ad.status = 'ENABLED' " +
          "AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'";
  var rows = AdsApp.search(q), ops = [], names = [];
  while (rows.hasNext()) {
    var r = rows.next();
    var d = r.adGroupAd.ad.responsiveSearchAd.descriptions || [];
    var pinned = d.filter(function (x) { return x.pinnedField; }).length;
    if (!pinned) { Logger.log(r.adGroup.name + ': no pins, skipped'); continue; }
    ops.push({ adOperation: { update: { resourceName: r.adGroupAd.ad.resourceName,
      responsiveSearchAd: { descriptions: d.map(function (x) { return { text: x.text }; }) } },
      updateMask: 'responsive_search_ad.descriptions' } });
    names.push(r.adGroup.name + ' (' + pinned + ' pins)');
  }
  if (!ops.length) { Logger.log('nothing to unpin'); return; }
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  res.forEach(function (x, i) { Logger.log(names[i] + ': ' + (x.isSuccessful() ? 'unpinned' : 'ERROR ' + x.getErrorMessages().join('; '))); });
}
