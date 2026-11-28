// One-off, 28 Nov 2026 (pf.gads): FIT page visitor list, attached to both FIT Search campaigns as OBSERVATION only.
// Observation never narrows who sees the ads; it lets Google report and learn on people who already saw /fit,
// and the list fills from today so YouTube Demand Gen can use or exclude it later. No spend, nothing enabled.
var CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
var CAMPAIGNS = ['24572169529', '24566018822']; // FIT Industry, FIT Brand
var LIST_NAME = 'FIT page visitors (trueyards.in/fit, 540 days)';

function main() {
  var existing = AdsApp.search("SELECT user_list.resource_name, user_list.name FROM user_list WHERE user_list.name = '" + LIST_NAME + "'");
  var listRn = existing.hasNext() ? existing.next().userList.resourceName : null;
  var ops = [];
  if (!listRn) {
    listRn = 'customers/' + CID + '/userLists/-1';
    ops.push({ userListOperation: { create: {
      resourceName: listRn,
      name: LIST_NAME,
      description: 'Anyone who opened trueyards.in/fit (FIT Industrial Township landing page)',
      membershipStatus: 'OPEN',
      membershipLifeSpan: 540,
      ruleBasedUserList: {
        prepopulationStatus: 'REQUESTED',
        flexibleRuleUserList: {
          inclusiveRuleOperator: 'AND',
          inclusiveOperands: [{ rule: { ruleItemGroups: [{ ruleItems: [{ name: 'url__', stringRuleItem: { operator: 'CONTAINS', value: 'trueyards.in/fit' } }] }] }, lookbackWindowDays: 540 }]
        }
      }
    } } });
  }
  CAMPAIGNS.forEach(function (c) {
    ops.push({ campaignOperation: { update: { resourceName: 'customers/' + CID + '/campaigns/' + c, targetingSetting: { targetRestrictions: [{ targetingDimension: 'AUDIENCE', bidOnly: true }] } }, updateMask: 'targeting_setting.target_restrictions' } });
  });
  CAMPAIGNS.forEach(function (c) {
    var has = AdsApp.search("SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.id = " + c + " AND campaign_criterion.type = 'USER_LIST'");
    if (has.hasNext()) { Logger.log('campaign ' + c + ' already has an audience, skipped'); return; }
    ops.push({ campaignCriterionOperation: { create: { campaign: 'customers/' + CID + '/campaigns/' + c, userList: { userList: listRn } } } });
  });
  if (!ops.length) { Logger.log('nothing to do'); return; }
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  res.forEach(function (r, i) { Logger.log('op ' + i + ': ' + (r.isSuccessful() ? 'OK ' + r.getResourceName() : 'ERROR ' + r.getErrorMessages().join('; '))); });
  // Confirm targeting stays observation (bid only) for audiences on both campaigns
  CAMPAIGNS.forEach(function (c) {
    var t = AdsApp.search("SELECT campaign.targeting_setting.target_restrictions FROM campaign WHERE campaign.id = " + c);
    Logger.log('campaign ' + c + ' targeting: ' + JSON.stringify(t.hasNext() ? t.next().campaign.targetingSetting : null));
  });
}
