# Bipartite Bard — Round 2 working archive

**Backed up:** 11 October 2026 (Round 2 runs 12–18 Oct; final build due **18 Oct 2026 23:59 IST**)
**Team:** Bipartite Bard — lead Anadi Tripathi (IIT Madras)
**Challenge:** The Sequential Matching Problem (Vouchsafe / RomeoJulietLove)

This archive exists because research material was lost twice — first the Round 1
`scripts/`, then this workspace's raw run data (it outgrew the snapshot cap).
**Everything in `00_`–`02_` is irreplaceable and exists nowhere else.**

---

## Directory map

| Folder | Contents | Replaceable? |
|---|---|---|
| `00_DELIVERABLE/` | `ROUND2_FINDINGS.md` (13 sections, the main doc), `ROUND2_PLAN.md` | **NO — irreplaceable** |
| `01_RESULTS/` | All computed analyses: 900-episode sweep, 720-episode ship run, Round-1-seed replication, soft-ask VM results, structural ceilings | **NO — irreplaceable** |
| `02_CODE/` | `waitlab.py` (harness), `analyse.py`, `ceilings.py`, `wait_comparison.py`, `round2_build/` (submission policy + Dockerfile) | **NO — irreplaceable** |
| `03_RAW_DATA/` | Per-episode / per-member JSONL, gzipped | Yes — regenerable from `02_CODE/` |
| `04_SOURCE_DOCS/` | Submitted Round 1 research PDF + extracted text | Yes, but keep |
| `05_OFFICIAL_KIT/` | Organiser release: `kit.py`, `evaluate.py`, `policy.py`, `PROBLEM_STATEMENT.md`, `docs/` | Yes — public repo |
| `06_UPLOADS/` | Files the lead attached during the project | Mostly yes |

**Regeneration:**
```bash
python3 02_CODE/waitlab.py --seeds 1101,1102 --arms greedy,oldest_first --workers 2 --out out/
python3 02_CODE/ceilings.py 1101,1102 development,sparse,cold_start,delayed,shift,drift
python3 02_CODE/analyse.py --out out --arms greedy,oldest_first
```

---

## Ship decision — `oldest_first` (decided 11 Oct, 720 episodes / 60 seeds)

`greedy` 0.412 vs `oldest_first` 0.399 — **diff +0.014, CI [−0.058, +0.085], p = 0.736. A tie.**

| arm | n | MSMI/100 | 95% CI | events | coverage | cov/ceil | ask |
|---|---:|---:|---:|---:|---:|---:|---:|
| `greedy` | 60 | **0.412** | [0.349, 0.479] | 297 | 0.336 | 0.979 | 199 |
| `oldest_first` | 60 | 0.399 | [0.332, 0.471] | 287 | 0.336 | 0.980 | 199 |

Decided on waiting time instead. Paired by seed, lower is better:

| metric | `greedy` | `oldest_first` | diff | 95% CI | verdict |
|---|---:|---:|---:|---|---|
| mean wait (served) | 6.871 | **6.641** | +0.230 | [+0.071, +0.389] | **oldest_first** |
| p90 wait (served) | 16.917 | **15.683** | **+1.233** | [+0.800, +1.683] | **oldest_first** |
| median wait (served) | **4.525** | 4.950 | −0.425 | [−0.708, −0.150] | greedy |
| unserved / 200 | 132.900 | 132.847 | +0.053 | [−0.167, +0.281] | tie |

FIFO gives up 0.43 days of median speed for the best-matched members and buys
**1.23 days off the p90 tail** — the statistic that answers "who gets left waiting".

### The number to lead the report with

The same code scored **0.489** on seeds 1101–1130 and **0.336** on seeds 1131–1160.

| arm | batch A (1101–1130) | batch B (1131–1160) | swing |
|---|---:|---:|---:|
| `greedy` | 0.489 | 0.336 | **−0.153** |
| `oldest_first` | 0.472 | 0.325 | **−0.147** |

Both arms swing together ⇒ world difficulty, not noise. Seed-set swing is
**9–14× the policy gap**. On the organiser's 20 private seeds, SE ≈ 0.06, so two
policies must differ by **~0.24** to be ranked reliably. Our gap is 0.014 —
**one tenth of a standard error**. Ranking near-identical policies on 20 seeds is
close to a coin flip; state this in the report.

### Safety checks (both pass)

- **Runtime:** 0.07 s per invocation vs the 10 s limit. A 1,595 s outlier in the
  batch run was sandbox CPU contention — **3.9 s per episode** when re-run alone.
- **Ask budget:** 4 hard bundles × 3 units = the official **12 units/day**. The cap
  binds on days 0–10; the askable pool drains to zero by day 20 under every rule.

---

## Reproducibility status — the thing that keeps getting lost

Round 1's PDF claims **1,326 episodes across 17 configurations**.
The largest surviving artifact is **360 episodes across 6 methods**.

**Verdict: a reproducibility failure, not an integrity failure.**

Evidence the 17-configuration numbers were genuinely computed (not fabricated):
- The Appendix B.9 funnel table has 7 mutually-constraining columns per method;
  **all 13 rows reconcile** internally.
- Implied stage rates reproduce the *separate* stage-rate table to 3–4 decimals
  (P(on-time | date) goes 0.194 greedy → 0.305 winner — the note's own central claim).
- The 5 methods common to both the 360-row core and the 17-config table **match exactly**.
- Pilot citations (thompson 0.472, gp_ucb 0.389, gp_mean 0.222) verified exactly.

**Where the code went:** three independent locations were searched — the VM bundle,
a Google Drive snapshot (9 Oct 08:03 IST), and a 47-file re-upload (all 47 byte-identical
to the repo). All three agree: the 13 scripts and 13 result artifacts were **never
persisted**. They lived only in live agent-session workspaces on deadline day and were
discarded when those sessions ended.

**Consequence:** *do not cite the 17-configuration numbers.* Rebuild on the
360-row reproducible core plus our own 1,620 episodes.

| Result | Status |
|---|---|
| `greedy` 0.350, `no_ask` 0.167, `random` 0.358, `max_weight_similarity` 0.408 | Reproduces exactly |
| `potential_ask` 0.525 (incumbent) | Reproduces **only after** fixing a signed-vs-unsigned agreement-score bug |
| `lab_potential_core4_maxw` 0.592 (Round 1 winner, best-of-17) | **No code anywhere — unreproducible** |
| `soft_ask_screen.py` | Present in repo, self-contained, reproduces |

**Lesson:** rebuilding a Round 1 configuration from the paper alone yields the *wrong*
policy. Always verify arm **semantics**, not just arm names.

---

## Other headline results

### Q1 confirmation — NON-REPLICATION

| | incumbent − greedy | 95% CI | seeds |
|---|---:|---:|---:|
| Round 1 note | **+0.175** | [+0.092, +0.258] | 10 |
| Parallel run | +0.008 | [−0.217, +0.233] | 10 |
| This run | **−0.044** | [−0.175, +0.081] | 30 |
| **Pooled** | **−0.031** | **[−0.143, +0.080]** | 40 |

**Never claim the incumbent beats greedy.**

### Why no learned scorer can help (a bound, not a gap)

Variance of the acceptance logit `z = −0.25 + bias + fit + shared + drift`:

| component | SD | share |
|---|---:|---:|
| `fit` — 4 soft-field agreements (**observable**) | 0.636 | **36.5%** |
| `bias` — per member, `N(0,0.7)` (**latent**) | 0.708 | 45.2% |
| `shared` — per pair, `N(0,0.45)` (**latent**) | 0.451 | 18.3% |

**64% of the variance is unobservable by construction** — unrecoverable by any model
from the policy interface. The observable 36.5% is exactly what we already use.

### Structural and null results

- **Disparity is world supply, not policy.** Reachable share by zone: a 0.48 / b 0.32 /
  c 0.23 / d 0.12 (4×). Gender (0.39/0.39/0.42) and age (0.37–0.42) are **flat** —
  negative controls, so the audit has power. Leg 2 (ask units) and Leg 3 (served | reachable)
  are flat for every group. Unfixable without overriding `acceptable_zones`.
- **Waiting is a null across arms.** The askable pool drains 45→0 by day 20 identically
  under *every* rule and the queue fully drains — reordering cannot change who waits.
- **Soft-ask lever is null (closed).** +0.0833 decomposes to **26 vs 23 events**
  (Poisson SD 7.0 ⇒ 0.43 SD); coverage +0.00028, assignments −0.17, ask cost **+44%**.
  Pooled with the 7-seed holdout: **68 vs 63 events over 120 paired episodes, p = 0.844.**
- **Generator:** `observe()` hides `exit_day` ⇒ batching cannot help. Joint acceptance
  0.2538 vs product of directionals 0.2297 (ratio 1.105) — **never multiply directionals**.
  No demographic term exists anywhere in the generator.
- **Seed blocks:** `delayed`/`shift`/`drift` share identical members with `development`
  per seed ⇒ ~90 independent worlds, not 180. **Seed is the only valid resampling unit.**
- **Ceilings (60 seeds):** development/delayed/shift/drift 0.389, sparse 0.171,
  cold_start 0.332. Per-seed development spread 0.260–0.500. All arms reach
  cov/ceil 0.979–0.980 ⇒ **report coverage ÷ ceiling, not raw coverage.**

---

## Still open

1. **Disclosure paragraph** — drafted, §11 of `ROUND2_FINDINGS.md`.
2. **Reproducibility-status table** — drafted, §12.
3. **`waitfloor` is contaminated** by the signed-ranking bug — relabel or re-run
   before it appears anywhere.
4. **Dockerfile has never been built** — must be before 18 Oct.
5. **Adaption Labs** (`adaptionlabs.ai`) — a general dataset-generation / AutoML
   platform. Given the 64% latent bound, it cannot change the approach.
   **Never share API keys or credentials with the agent.**

## Hygiene rules learned the hard way

- Keep the workspace **under ~100 MB**; raw JSONL is what gets pruned first.
- Extract summaries to `ROUND2_FINDINGS.md` **immediately**, then gzip or delete raw JSONL.
- Re-archive to a zip at the end of every session, and **download the zip**.
- A resumed run can silently skip episodes if arm *names* match but semantics don't —
  verify semantics, not names.
