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
| `00_DELIVERABLE/` | `ROUND2_FINDINGS.md` (10 sections, the main doc), `ROUND2_PLAN.md` | **NO — irreplaceable** |
| `01_RESULTS/` | All computed analyses: 900-episode sweep, Round-1-seed replication, fidelity checks, soft-ask VM results | **NO — irreplaceable** |
| `02_CODE/` | `waitlab.py` (harness), `analyse.py`, `ceilings.py`, `round2_build/` (submission policy + Dockerfile) | **NO — irreplaceable** |
| `03_RAW_DATA/` | Per-episode / per-member JSONL, gzipped. `INCOMPLETE_60seed_run/` was mid-write when archived. | Yes — regenerable from `02_CODE/` |
| `04_SOURCE_DOCS/` | Submitted Round 1 research PDF + extracted text | Yes, but keep |
| `05_OFFICIAL_KIT/` | Organiser release: `kit.py`, `evaluate.py`, `policy.py`, `PROBLEM_STATEMENT.md`, `docs/` | Yes — public repo |
| `06_UPLOADS/` | Files the lead attached during the project | Mostly yes |

**Regeneration command** (any arm, any seeds):
```bash
python3 02_CODE/waitlab.py --seeds 1101,1102 --arms greedy,oldest_first --workers 2 --out out/
python3 02_CODE/analyse.py --out out/
```

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

**Consequence for Round 2:** *do not cite the 17-configuration numbers.* Rebuild on the
360-row reproducible core plus our own 900-episode run.

### What reproduces today

| Result | Status |
|---|---|
| `greedy` 0.350, `no_ask` 0.167, `random` 0.358, `max_weight_similarity` 0.408 | Reproduces exactly |
| `potential_ask` 0.525 (incumbent) | Reproduces **only after** fixing a signed-vs-unsigned agreement-score bug |
| `lab_potential_core4_maxw` 0.592 (Round 1 winner, best-of-17) | **No code anywhere — unreproducible** |
| `soft_ask_screen.py` | Present in repo, self-contained, reproduces |

**Lesson:** rebuilding a Round 1 configuration from the paper alone yields the *wrong*
policy. Always verify arm **semantics**, not just arm names.

---

## Headline results

### Q1 confirmation — NON-REPLICATION

| | incumbent − greedy | 95% CI | seeds |
|---|---:|---:|---:|
| Round 1 note | **+0.175** | [+0.092, +0.258] | 10 |
| Parallel run | +0.008 | [−0.217, +0.233] | 10 |
| This run | **−0.044** | [−0.175, +0.081] | 30 |
| **Pooled** | **−0.031** | **[−0.143, +0.080]** | 40 |

`greedy` scored **0.358 vs 0.489** on disjoint seed sets — 0.13 of pure seed variation.
**Never claim the incumbent beats greedy.**

### 30 fresh seeds (1101–1130), 900 episodes

```
greedy (official)    0.489 [0.397,0.586] 176ev cov/ceil 0.979
oldest_first (new)   0.472 [0.386,0.558] 170ev cov/ceil 0.982
potential_ask (inc.) 0.444 [0.342,0.544] 160ev cov/ceil 0.979
waitfloor (new)      0.372 [0.283,0.461] 134ev   [CONTAMINATED]
signed_potential     0.372 [0.283,0.461] 134ev
```

Per-seed SD of (greedy − incumbent) is **0.365**; at 10 seeds SE ≈ 0.115, so **nothing
under ≈0.23 is resolvable**. The only interval excluding zero: `waitfloor` < `oldest_first` (p=0.039).
`waitfloor` ran under a signed-ranking bug — relabel or re-run before publishing.

### Why no learned scorer can help (a bound, not a gap)

Variance of the acceptance logit `z = −0.25 + bias + fit + shared + drift`:

| component | SD | share |
|---|---:|---:|
| `fit` — 4 soft-field agreements (**observable**) | 0.636 | **36.5%** |
| `bias` — per member, `N(0,0.7)` (**latent**) | 0.708 | 45.2% |
| `shared` — per pair, `N(0,0.45)` (**latent**) | 0.451 | 18.3% |

**64% of the variance is unobservable by construction** — unrecoverable by any model
from the policy interface. The observable 36.5% is exactly what we already use.

### Other results

- **Disparity is world supply, not policy.** Reachable share by zone: a 0.48 / b 0.32 /
  c 0.23 / d 0.12 (4×). Gender (0.39/0.39/0.42) and age (0.37–0.42) are **flat** —
  negative controls, so the audit has power. Leg 2 (ask units) and Leg 3 (served | reachable)
  are flat for every group. Unfixable without overriding `acceptable_zones`.
- **Waiting is a null.** Means 6.20–6.83 d, p90 16–17, spread 0.46 d across arms.
  The askable pool drains 45→0 by day 20 identically under *every* rule, and the queue
  fully drains — so reordering cannot change who waits.
- **Soft-ask lever is null (closed).** `hard_plus_soft_maxweight` 0.7222 vs 0.6389 (+0.0833)
  decomposes to **26 vs 23 events** (Poisson SD 7.0 ⇒ 0.43 SD); coverage +0.00028,
  assignments −0.17, ask cost **+44%**. Effect lives only in cold_start (+0.333) and
  delayed (+0.167); 4/6 families exact ties. Pooled with the 7-seed holdout:
  **68 vs 63 events over 120 paired episodes, 0.44 SD, p = 0.844.**
- **Generator:** `observe()` hides `exit_day` ⇒ batching cannot help. Joint acceptance
  0.2538 vs product of directionals 0.2297 (ratio 1.105) — **never multiply directionals**.
  No demographic term exists anywhere in the generator.
- **Seed blocks:** `delayed`/`shift`/`drift` share identical members with `development`
  per seed ⇒ ~90 independent worlds, not 180. **Seed is the only valid resampling unit.**
- **Ceilings (30 seeds):** development 0.395, sparse 0.169, cold_start 0.326,
  delayed/shift/drift 0.395. All arms reach cov/ceil 0.976–0.984 ⇒ report coverage ÷ ceiling, not raw coverage.

---

## Still open

1. **60-seed `greedy` vs `oldest_first`** — the ship tie-break. Was mid-run when this
   archive was taken; results land in `ROUND2_FINDINGS.md`.
2. **Disclosure paragraph** — one paragraph stating the 17-configuration layer is not
   reproducible and is not cited.
3. **Reproducibility-status table** for the report (above).
4. **Dockerfile has never been built** — must be before 18 Oct.
5. **Adaption Labs** (`adaptionlabs.ai`) — organisers mentioned it. It is a general
   dataset-generation / AutoML platform. Given the 64% latent bound above, it cannot
   change the approach. **Never share API keys or credentials with the agent.**

## Hygiene rules learned the hard way

- Keep the workspace **under ~100 MB**; raw JSONL is what gets pruned first.
- Extract summaries to `ROUND2_FINDINGS.md` **immediately**, then delete raw JSONL.
- A resumed run can silently skip episodes if arm *names* match but semantics don't —
  verify semantics, not names.
