# Round 2 fresh-seed confirmation and component analysis

Team Bipartite Bard · 10 October 2026 · public simulator only, in-process.
Design frozen in [`ROUND2_PRE_REGISTRATION.md`](ROUND2_PRE_REGISTRATION.md)
before the first episode; machine results in
[`results/round2_analysis.json`](../results/round2_analysis.json); raw rows in
`results/round2_shard_0of2.json` + `results/round2_shard_1of2.json`
(360/360 episodes valid). Ten genuinely new seeds (1111 to 2020) × six families;
seed blocks (six scenarios sharing a world) are the resampling unit everywhere;
bootstrap percentile CIs (10,000 draws, seed 20261010), exact sign-flip p,
W/T/L over the 60 paired episodes; no multiplicity adjustment, stated.

## 1. Confirmation (Q1): the incumbent edge does not survive new worlds

`potential_ask − greedy` on the ten fresh seeds is **+0.008 MSMI/100,
95% seed-block CI [−0.217, +0.233], sign-flip p = 1.000, W/T/L 14/27/19**.
By the pre-registered failure rule (CI includes zero and estimate below +0.05)
the chosen configuration is **not confirmed** on genuinely new worlds. This is
the selection-bias caveat from the Round 1 note resolving as predicted: the
same contrast was +0.175 on the ten screen seeds and +0.143 on the seven
least-selected of them, and +0.008 once the worlds are truly new. Greedy itself
is stable across seed sets (0.350 → 0.358); the incumbent moved (0.525 →
0.367). We report this as the headline, not a burying.

What does survive is the step function: `greedy − no_ask` is **+0.292,
CI [+0.108, +0.483], p = 0.023, 27/29/4** (Round 1: +0.183). Asking at all,
however naively, remains the only robust lever; fresh-seed primaries:

| Configuration | Fresh-seed primary | 95% CI | Round 1 (10 screen seeds) |
|---|---:|---|---:|
| Potential asks · global match (incumbent) | 0.367 | [0.192, 0.558] | 0.525 |
| Potential asks · greedy ordering | 0.442 | [0.267, 0.617] | 0.467 |
| Greedy + default asks (official) | 0.358 | [0.225, 0.517] | 0.350 |
| Max-weight similarity | 0.258 | [0.142, 0.400] | 0.408 |
| Random feasible (official) | 0.208 | [0.100, 0.325] | 0.358 |
| No clarification (official) | 0.067 | [0.000, 0.183] | 0.167 |

## 2. Interactions (Q2): nothing survives except the ask step

Fresh-seed factorial effects (seed-block CIs): ask main **+0.096 [−0.088,
+0.288]**, allocation main **−0.088 [−0.204, +0.038]**, ask×allocation
interaction **+0.025 [−0.200, +0.267]**; all three straddle zero. Pooling the
allocation effect with its Round 1 value (+0.058 on screen seeds) gives about
−0.015 over twenty seed blocks: **global maximum-weight matching adds nothing
on average over greedy ordering**, and the count-based ask rule adds nothing
over greedy ordering beyond asking at all. The simpler method
(potential asks + greedy ordering, no blossom matching) is statistically
indistinguishable from the full stack on fresh worlds and numerically *above*
it here (0.442 vs 0.367).

**What the comparison taught us.** Round 1's +0.058 allocation effect and the
incumbent's edge were both fitted to the same ten public seeds; out of sample
they shrink through zero in opposite directions, which is the signature of
noise plus selection, not of small true effects. The components that transfer
are the two cheapest ones: ask something (any rule), and consume the edge
supply early. Everything we invested in between those two steps (targeting,
weighting, global allocation, online adaptation) is third-order, exactly as
the structural diagnosis predicted, and now confirmed on worlds no design
decision ever saw.

## 3. Calibration and who gets left waiting (Q3)

Analysis-only world audit on the twenty fresh worlds (latents read from the
generator for diagnosis; no policy sees them):

- **Missingness confound, out of sample.** Mean latent response rate is flat
  across observability groups (0.758 / 0.764 / 0.758 for none / some / all
  hard fields observed), while the declined-hard-field share is 74% / 70% /
  1%. Observability selects *who is askable*, not *who is compatible*: the
  generator has no demographic or observability effect on preferences, and
  the Round 1 fitted prior's lowest-bin miscalibration (predicted 0.090,
  observed 0.157) is precisely this confound, now reproduced on new worlds.
- **Who waits.** `no_ask` serves 25 of 200 members with a 3.55-day mean wait;
  every asking rule serves about 65 (unserved 134.9 to 135.4) at 6.3 to 7.0
  days. The unserved composition is a world property, not a rule property:
  declined-blocked shares (about 32 to 41% by family) and observed-degree-zero
  shares (53% of fully-observed development members, 87% in sparse) are
  identical inputs to every rule, and the four asking rules' unserved counts
  agree to within 0.5 members. Rules change *whether* members wait, not *who*
  waits; the pre-registered expectation (never-served sets dominated by the
  world's infeasible core) holds.
- **Changing conditions.** Per-family fresh primaries keep the Round 1
  pattern: sparse is supply-limited for everyone (0.00 to 0.10), cold start
  again favours greedy ordering (0.50 vs 0.25 for the incumbent), shift/drift
  are the richest worlds (0.60 to 0.65). Delayed behaves like development.

## 4. Scope and limitations

Six configurations are exactly the ones reproducible from this repository; the
unlock/prior/online variants live in the author's pending `scripts/policies.py`
and join the factorial once pushed. Timings are in-process, not container-mode.
Per-member served identities are not in the row-level data, so the who-waits
audit bounds rule differences by the world's infeasible core rather than
computing a served-set Jaccard; labelled as such. No private seeds, no private
evaluation, no real-user data.
