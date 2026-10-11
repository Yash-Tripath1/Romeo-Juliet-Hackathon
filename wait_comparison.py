import json, statistics, random
from collections import defaultdict
arms = {'greedy', 'oldest_first'}
VAR = ('development','sparse','cold_start','delayed','shift','drift')
waits   = defaultdict(list)   # (arm, seed) -> [wait of each served member]
unserv  = defaultdict(int)    # (arm, seed, variant) -> count never introduced
tot     = defaultdict(int)

for line in open('out/members.jsonl'):
    line = line.strip()
    if not line: continue
    r = json.loads(line); a = r['arm']
    if a not in arms: continue
    kv = (a, r['seed'], r['variant'])
    tot[kv] += 1
    if r.get('fid') is None: unserv[kv] += 1
    else:                    waits[(a, r['seed'])].append(r['wait'])

seeds = sorted({s for (_, s) in waits})
def pct(v, p):
    v = sorted(v); return v[min(len(v)-1, int(p*len(v)))]
def boot(d, n=20000, seed=13):
    r = random.Random(seed); x = list(d.values()); k = len(x)
    dr = sorted(statistics.fmean(r.choices(x, k=k)) for _ in range(n))
    return statistics.fmean(x), dr[int(.025*n)], dr[int(.975*n)]

metrics = [
    ("mean wait (served)", lambda a,s: statistics.fmean(waits[(a,s)])),
    ("median wait (served)",lambda a,s: statistics.median(waits[(a,s)])),
    ("p90 wait (served)",   lambda a,s: pct(waits[(a,s)], .90)),
    ("max wait (served)",   lambda a,s: max(waits[(a,s)])),
    ("unserved / 200",      lambda a,s: statistics.fmean(unserv[(a,s,v)] for v in VAR)),
]
print("="*94)
print("WAITING TIME  --  the Round 2 criterion that could break the tie")
print("(pooled over 60 seeds x 6 variants; served = got >=1 introduction; paired by seed)")
print("="*94)
print(f"{'metric':22s} {'greedy':>8s} {'oldest':>8s} {'diff':>8s} {'95% CI':>18s} {'W/T/L':>12s}  verdict")
print("-"*94)
for name, fn in metrics:
    d = {s: fn('greedy', s) - fn('oldest_first', s) for s in seeds}
    m, lo, hi = boot(d)
    g = statistics.fmean(fn('greedy', s)      for s in seeds)
    o = statistics.fmean(fn('oldest_first', s) for s in seeds)
    w = sum(1 for v in d.values() if v >  1e-9)
    l = sum(1 for v in d.values() if v < -1e-9)
    verdict = "GREEDY higher" if lo > 0 else ("OLDEST_FIRST higher" if hi < 0 else "tie")
    print(f"{name:22s} {g:8.3f} {o:8.3f} {m:+8.3f} [{lo:+.3f},{hi:+.3f}] {w:4d}/{len(d)-w-l:3d}/{l:4d}  {verdict}")
print("-"*94)
print("  For waits, LOWER is better. 'GREEDY higher' = oldest_first is the kinder queue.")
