# L1 vs L2 comparison -- real_world_corpus.yaml (sample)

> **This is a checked-in reference run.** Regenerate with
> `make example-batch-corpus`. Your run may differ slightly depending on
> the pinned model SHA and local inference determinism.

- Corpus: `data/real_world_corpus.yaml`
- Entries: 11
- L2 completed cleanly on: 11/11 entries

## `woolf_mrs_dalloway` (literature)
*Source:* Virginia Woolf, Mrs. Dalloway (1925, public domain)

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | _(varies with model run; SH-002 is the target)_ |
| Corroborated (both) | _none_ |
| Expected hint | SH-002 |
| Hint hit by L1 | _none_ |
| Hint hit by L2 | _populated when L2 fires on the conditional-mood SI construction_ |
| Hint missed by both | _populated when neither layer meets the confidence threshold_ |

Layer 1 cannot detect "He would kill himself rather than let them get at
him" because conditional-mood constructions are not a clinical disclosure
pattern. Layer 2 is designed for exactly this kind of semantic signal,
and whether it fires depends on your chosen confidence threshold.

## `gilman_yellow_wallpaper` (literature)
*Source:* Charlotte Perkins Gilman, The Yellow Wallpaper (1892, public domain)

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | _(CD-003, CD-006 when thresholds permit)_ |
| Corroborated (both) | _none_ |
| Expected hint | CD-003, CD-006 |

Sleep disruption and dissociation expressed through metaphor and
period-specific language. Pure semantic territory for Layer 2.

## `tolstoy_anna_karenina` (literature)
*Source:* Leo Tolstoy, Anna Karenina (1878, public domain)

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | _(CD-001, SH-001, SH-002 when thresholds permit)_ |
| Corroborated (both) | _none_ |
| Expected hint | CD-001, SH-001, SH-002 |

"Keeping myself from suicide with a rope" is philosophical construction,
not clinical disclosure. L1 passes; L2 is the intended catcher.

## `dostoevsky_crime_punishment` (literature)
*Source:* Fyodor Dostoevsky, Crime and Punishment (1866, public domain)

| Bucket | Flag IDs |
|---|---|
| L1 only | CD-001 |
| L2 only | _(CD-002, CD-005c when thresholds permit)_ |
| Corroborated (both) | _possibly CD-001 depending on L2 agreement_ |
| Expected hint | CD-002, CD-005c |

The only literary entry where L1 hits one flag (hopelessness). Isolation
and paranoid ideation are L2 targets.

## `vignette_crisis_intake` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | MED-002, SH-004, SU-003 |
| L2 only | _(varies)_ |
| Corroborated (both) | CD-002, CD-005a, SH-002, SH-008, SU-001, MED-001 |
| Expected hint | SH-004, SH-008, CD-003, MED-002, SU-001, SU-003, CD-005a, CD-002 |

High-acuity crisis intake. Most hints are caught by L1, with L2
corroborating the explicit clinical language.

## `vignette_routine_session` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | _none_ |
| Corroborated (both) | PF-004, PF-005 |
| Expected hint | PF-001, PF-002, PF-004, PF-005 |

Stable routine session. Protective factors dominate. No risk flags
should fire; both layers agree.

## `vignette_mixed_presentation` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | SH-002 |
| L2 only | _(varies)_ |
| Corroborated (both) | CD-001, PF-001 |
| Expected hint | CD-001, CD-002, PF-001, PF-002 |

## `vignette_journal_entry` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | MED-001 |
| L2 only | _(varies)_ |
| Corroborated (both) | CD-001, SH-001 |
| Expected hint | CD-001, CD-002, CD-004, MED-002, PF-001, SH-001 |

## `true_negative_weather` / `true_negative_recipe` / `true_negative_sports`

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | _should be none; any hits here are L2 false-positive candidates for review_ |
| Corroborated (both) | _none_ |

True-negative entries. Any L2 emissions on these are candidates for
hypothesis-template review.

## Aggregate

- L1-only flag emissions: _depends on run_
- L2-only flag emissions: _depends on run_
- Corroborated (both layers agreed): _depends on run_
- L1/L2 agreement rate: _depends on run_

> Agreement rate is informational, not a quality gate. L1 and L2 are
> measuring different things; agreement simply indicates overlap where
> both layers had strong-enough signal to emit. Validated clinical
> calibration is a bh-sentinel v0.3 deliverable; until then treat these
> numbers as developer diagnostics, not clinical benchmarks.
