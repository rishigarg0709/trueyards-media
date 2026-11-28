// One-off, 28 Nov 2026 (pf.gads). Rishi 18:16: promote the two uploaded Shorts; 18:17: use main gate images.
// 1) Image assets (2 drone + 2 main gate) linked to both FIT Search campaigns.
// 2) YouTube Demand Gen campaign "FIT Industry - YouTube", built PAUSED, INR 450 a day (D77), YouTube only
//    (Shorts, in-feed, in-stream), same locations as FIT Industry Search, English and Hindi, landing trueyards.in/fit.
var CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
var C = 'customers/' + CID;
var RAW = 'https://raw.githubusercontent.com/rishigarg0709/trueyards-media/main/ads/creatives/fit-google/';
var SEARCH = ['24572169529', '24566018822'];
var VIDEOS = [['C3Ikdm12gx0', 'FIT Short P10 plot mil gayi'], ['-I7Fc52KZLY', 'FIT Short P12 apni factory ka address']];
var URL = 'https://trueyards.in/fit?utm_source=youtube&utm_medium=video&utm_campaign=fit_youtube_demandgen';

function img(name, file, rn) {
  var b = UrlFetchApp.fetch(RAW + file).getBlob().getBytes();
  return { assetOperation: { create: { resourceName: rn, name: name, type: 'IMAGE', imageAsset: { data: Utilities.base64Encode(b) } } } };
}

function main() {
  var ops = [];
  // ---- Search image assets
  var imgs = [['FIT drone wide', 'fit-drone-191x1.jpg'], ['FIT drone square', 'fit-drone-1x1.jpg'],
              ['FIT main gate wide', 'fit-gate-191x1.jpg'], ['FIT main gate square', 'fit-gate-1x1.jpg']];
  imgs.forEach(function (x, i) {
    var rn = C + '/assets/-' + (20 + i);
    ops.push(img(x[0], x[1], rn));
    SEARCH.forEach(function (c) { ops.push({ campaignAssetOperation: { create: { campaign: C + '/campaigns/' + c, asset: rn, fieldType: 'AD_IMAGE' } } }); });
  });
  // ---- Demand Gen
  var bud = C + '/campaignBudgets/-1', camp = C + '/campaigns/-2', ag = C + '/adGroups/-3', logo = C + '/assets/-6';
  ops.push({ campaignBudgetOperation: { create: { resourceName: bud, name: 'FIT Industry - YouTube budget', amountMicros: 450000000, deliveryMethod: 'STANDARD', explicitlyShared: false } } });
  ops.push({ campaignOperation: { create: { resourceName: camp, name: 'FIT Industry - YouTube', advertisingChannelType: 'DEMAND_GEN', status: 'PAUSED',
    campaignBudget: bud, targetSpend: {}, containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' } } });
  // same positive locations as FIT Industry Search, plus English and Hindi
  var geo = AdsApp.search("SELECT campaign_criterion.location.geo_target_constant, campaign_criterion.negative FROM campaign_criterion WHERE campaign.id = 24572169529 AND campaign_criterion.type = 'LOCATION'");
  while (geo.hasNext()) {
    var g = geo.next().campaignCriterion; var id = g.location.geoTargetConstant.split('/').pop();
    ops.push({ campaignCriterionOperation: { create: { resourceName: C + '/campaignCriteria/-2~' + id, campaign: camp, negative: !!g.negative, location: { geoTargetConstant: g.location.geoTargetConstant } } } });
  }
  [1000, 1023].forEach(function (l) { ops.push({ campaignCriterionOperation: { create: { resourceName: C + '/campaignCriteria/-2~' + l, campaign: camp, language: { languageConstant: 'languageConstants/' + l } } } }); });
  ops.push({ adGroupOperation: { create: { resourceName: ag, campaign: camp, name: 'FIT Shorts P10 and P12', status: 'ENABLED',
    demandGenAdGroupSettings: { channelControls: { selectedChannels: { youtubeInStream: true, youtubeInFeed: true, youtubeShorts: true, discover: false, gmail: false, display: false } } } } } });
  var vids = VIDEOS.map(function (v, i) { var rn = C + '/assets/-' + (4 + i); ops.push({ assetOperation: { create: { resourceName: rn, name: v[1], youtubeVideoAsset: { youtubeVideoId: v[0] } } } }); return { asset: rn }; });
  ops.push(img('FIT logo square', 'fit-logo-1x1.jpg', logo));
  function t(a) { return a.map(function (x) { return { text: x }; }); }
  ops.push({ adGroupAdOperation: { create: { adGroup: ag, status: 'ENABLED', ad: { name: 'FIT Shorts P10 and P12', finalUrls: [URL],
    demandGenVideoResponsiveAd: {
      headlines: t(['Industrial Plots Near Rohtak', 'Your Factory Address in Haryana', 'FIT Industrial Township', '400 to 4,000 Sq Yd Plots', 'Book a Free Site Visit']),
      longHeadlines: t(['138-acre planned industrial township at Kalanaur, Rohtak, 10 min from NH-152D.']),
      descriptions: t(['Own substation, STP and 18 m and 24 m roads. Get the site plan on WhatsApp in minutes.']),
      businessName: { text: 'FIT by Forteasia' }, videos: vids, logoImages: [{ asset: logo }] } } } } });
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var ok = 0;
  res.forEach(function (r, i) {
    if (r.isSuccessful()) { ok++; if (/campaigns\/|adGroupAds|adGroups\//.test(r.getResourceName() || '')) Logger.log('OK ' + r.getResourceName()); }
    else Logger.log('ERROR op ' + i + ' ' + Object.keys(ops[i])[0] + ': ' + r.getErrorMessages().join('; '));
  });
  Logger.log('ops ' + ops.length + ', ok ' + ok);
}
