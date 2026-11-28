// One-off, 28 Nov 2026 (pf.gads). Rishi 18:17 and 18:19: use the main gate images and the Gemini 3D/realistic images.
// Adds image assets to both FIT Search campaigns, and logs what the existing YouTube Demand Gen campaign holds.
var CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, ''), C = 'customers/' + CID;
var RAW = 'https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/ads/creatives/fit-google/';
var SEARCH = ['24572169529', '24566018822'];
var IMGS = ['fit-gate-191x1', 'fit-gate-1x1', 'fit-drone-191x1', 'fit-drone-1x1', 'fit-ai-factory-191x1', 'fit-ai-factory-1x1',
  'fit-ai-aerial-191x1', 'fit-ai-aerial-1x1', 'fit-ai-model-warehouse-191x1', 'fit-ai-model-warehouse-1x1',
  'fit-ai-factory-night-191x1', 'fit-ai-model-township-191x1'];
function main() {
  var ops = [];
  IMGS.forEach(function (f, i) {
    var rn = C + '/assets/-' + (20 + i);
    var b = UrlFetchApp.fetch(RAW + f + '.jpg').getBlob().getBytes();
    ops.push({ assetOperation: { create: { resourceName: rn, name: 'FIT ' + f + ' ' + i, type: 'IMAGE', imageAsset: { data: Utilities.base64Encode(b) } } } });
    SEARCH.forEach(function (c) { ops.push({ campaignAssetOperation: { create: { campaign: C + '/campaigns/' + c, asset: rn, fieldType: 'AD_IMAGE' } } }); });
  });
  var res = AdsApp.mutateAll(ops, { partialFailure: true }), ok = 0;
  res.forEach(function (r, i) { if (r.isSuccessful()) ok++; else Logger.log('ERROR op ' + i + ': ' + r.getErrorMessages().join('; ')); });
  Logger.log('images: ops ' + ops.length + ', ok ' + ok);
  var q = "SELECT campaign.id, campaign.name, ad_group.name, ad_group.status, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, " +
    "ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.business_name FROM ad_group_ad WHERE campaign.advertising_channel_type = 'DEMAND_GEN'";
  var it = AdsApp.search(q);
  while (it.hasNext()) { var r = it.next(); Logger.log('DG ' + JSON.stringify({ c: r.campaign.id, g: r.adGroup.name, gs: r.adGroup.status, s: r.adGroupAd.status, ap: r.adGroupAd.policySummary.approvalStatus, ad: r.adGroupAd.ad })); }
  var v = AdsApp.search("SELECT asset.resource_name, asset.youtube_video_asset.youtube_video_id, asset.name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'");
  while (v.hasNext()) { var a = v.next().asset; Logger.log('VID ' + a.resourceName + ' ' + a.youtubeVideoAsset.youtubeVideoId + ' ' + a.name); }
}
