#!/usr/bin/env python3
"""Per-seed structural coverage ceiling (ANALYSIS ONLY).

Ceiling = fraction of members arrived by day 59 who have at least one
feasible partner under complete disclosure, neither endpoint decline-blocked.
This is what a policy with free, perfect, instantaneous clarification would
reach. No policy may use this; it is computed from the world after the fact.
Round 1 reported a 10-seed mean; the per-seed column was left pending.
"""
import sys, json, itertools, copy
sys.path.insert(0,'/home/user/work/official')
from kit import generate, eligibility, HARD

def ceiling(seed, variant, n=200):
    w = generate(seed, n, 'evaluation', variant)
    for m in w['members']:
        for f,v in m['truth'].items():
            if m['field_status'].get(f)!='declined': m['fields'][f]=v
    ms = [m for m in w['members'] if m['arrived_day']<=59]
    blocked = {m['member_id'] for m in ms if any(m['field_status'].get(f)=='declined' for f in HARD)}
    deg = {m['member_id']:0 for m in ms}
    for a,b in itertools.combinations(ms,2):
        if a['member_id'] in blocked or b['member_id'] in blocked: continue
        if eligibility(a,b)['status']=='feasible':
            deg[a['member_id']]+=1; deg[b['member_id']]+=1
    coverable = sum(1 for m in ms if m['member_id'] not in blocked and deg[m['member_id']]>0)
    eff_edges = sum(1 for a,b in itertools.combinations(ms,2)
                    if a['member_id'] not in blocked and b['member_id'] not in blocked
                    and eligibility(a,b)['status']=='feasible')
    return {'seed':seed,'variant':variant,'arrived':len(ms),
            'ceiling':coverable/max(1,len(ms)),'degree0':sum(1 for m in ms if deg[m['member_id']]==0)/max(1,len(ms)),
            'decline_blocked':len(blocked)/max(1,len(ms)),'effective_edges':eff_edges,
            'mean_degree':sum(deg[m['member_id']] for m in ms)/max(1,len(ms))}

if __name__=='__main__':
    seeds=[int(x) for x in sys.argv[1].split(',')]
    variants=sys.argv[2].split(',')
    out=[ceiling(s,v) for v in variants for s in seeds]
    json.dump(out, open('out/ceilings.json','w'), indent=1)
    import statistics
    print(f"{'variant':12s} {'ceiling':>8s} {'deg0':>7s} {'declined':>9s} {'edges':>7s} {'mean_deg':>9s}   (mean over {len(seeds)} seeds)")
    for v in variants:
        rs=[o for o in out if o['variant']==v]
        print(f"{v:12s} {statistics.fmean(o['ceiling'] for o in rs):8.3f} "
              f"{statistics.fmean(o['degree0'] for o in rs):7.3f} "
              f"{statistics.fmean(o['decline_blocked'] for o in rs):9.3f} "
              f"{statistics.fmean(o['effective_edges'] for o in rs):7.1f} "
              f"{statistics.fmean(o['mean_degree'] for o in rs):9.2f}")
    print()
    print('per-seed development ceilings:', ' '.join(f"{o['seed']}:{o['ceiling']:.3f}" for o in out if o['variant']=='development'))
