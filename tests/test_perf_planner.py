"""python3 tests/test_perf_planner.py : media planner rules."""
import os, sys, json
sys.path.insert(0, "scripts")
import perf_planner as P

C = P.CFG
def ev(wa, meta):
    out = {}
    for k, (spend, q, v, l) in (("wa", wa), ("meta", meta)):
        out[k] = {"spend": spend, "qualified": q, "visit_planned": v, "leads": l, "visit_done": 0, "booked": 0,
                  "per_visit": round(spend / v) if v else None, "per_qualified": round(spend / q) if q else None, "per_lead": round(spend / l) if l else None}
    return out

# first plan: start shares
wa, meta, r = P.split_channels(1500, None, {}, 0)
assert (wa, meta) == (1005, 495), (wa, meta)
# not enough evidence: unchanged
prev = {"total": 1500, "wa_budget_inr": 1000, "meta_budget_inr": 500}
wa, meta, r = P.split_channels(1500, prev, ev((14000, 4, 1, 280), (7000, 2, 0, 90)), 20)
assert (wa, meta) == (1000, 500) and "Not enough" in r[0], r
# Meta cheaper per visit, mature: money moves to Meta, at most 20% of total
wa, meta, r = P.split_channels(1500, prev, ev((14000, 30, 10, 280), (7000, 30, 10, 140)), 20)
assert meta > 500 and meta - 500 <= 300 and wa + meta == 1500, (wa, meta, r)
# Meta worse but young: protected
wa, meta, r = P.split_channels(1500, prev, ev((7000, 30, 10, 280), (7000, 10, 3, 90)), 7)
assert (wa, meta) == (1000, 500) and "days old" in r[0], r
# WhatsApp worse: cut, never below its floor (30% of its start share)
prev2 = {"total": 1500, "wa_budget_inr": 320, "meta_budget_inr": 1180}
wa, meta, r = P.split_channels(1500, prev2, ev((7000, 10, 3, 90), (7000, 40, 12, 280)), 60)
assert wa >= round(1500 * C["start_share"]["wa"] * C["floor_of_start"]) - 1, (wa, r)
# noise: close costs, no shift
wa, meta, r = P.split_channels(1500, prev, ev((10000, 20, 10, 200), (10500, 20, 10, 150)), 30)
assert (wa, meta) == (1000, 500), r
# total changed: proportions kept
wa, meta, r = P.split_channels(3000, prev, {}, 30)
assert (wa, meta) == (2000, 1000), (wa, meta)
print("ok channels")

# Meta tactics
b, sh, r = P.split_meta(500, {"schedule": []}, {}, {}, None)
assert b.get("warm", 0) == 0 and sum(b.values()) == 500, b
summ = {"schedule": [{"d0": "2026-12-01"}], "lift": {"all": {"all": {"waves": 4, "wd": 800, "wl": 30, "cd": 800, "cl": 15, "lift": 1.6}}}}
b1, sh1, r1 = P.split_meta(600, summ, {"warm": {"spend": 600}, "remind": {"spend": 150}}, {"wa": {"per_lead": 60}}, None)
assert sh1["warm"] > C["meta_tactics_start"]["warm"] / sum(C["meta_tactics_start"].values()) - 1e-9 and "pays" in r1[0], (sh1, r1)
summ["lift"]["all"]["all"].update(wl=16, lift=1.05)
b2, sh2, r2 = P.split_meta(600, summ, {"warm": {"spend": 900}}, {"wa": {"per_lead": 60}}, None)
assert sh2["warm"] < sh1["warm"] and "not paying" in r2[0], (sh2, r2)
assert sum(b2.values()) == 600
b3, _, r3 = P.split_meta(200, {"schedule": [{"d0": "x"}]}, {}, {}, None)
assert all(v == 0 or v >= C["min_tactic_inr"] for v in b3.values()) and sum(b3.values()) == 200, (b3, r3)
print("ok tactics")

# awaiting total: nothing changes
os.makedirs("/tmp/pp", exist_ok=True)
cwd = os.getcwd(); os.chdir("/tmp/pp"); P.CFG = dict(C, total_daily_inr=None)
out = P.plan()
assert out["status"] == "awaiting_total" and "wa_budget_inr" not in out
os.chdir(cwd)
print("all planner tests passed")
