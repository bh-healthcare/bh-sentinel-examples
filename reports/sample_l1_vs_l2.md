# L1 vs L2 comparison -- real_world_corpus.yaml

- Generated: `2026-05-30T13:26:15.844343+00:00`
- Corpus: `/Users/tanmayakumar/Development/bh-healthcare/bh-sentinel-examples/data/real_world_corpus.yaml`
- Entries: 11
- L2 completed cleanly on: 11/11 entries

## `woolf_mrs_dalloway` (literature)
*Source:* Virginia Woolf, Mrs. Dalloway

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-005a, CD-005b, CD-005c, CD-006, HO-001, HO-002, HO-003, HO-004, HO-005, HO-006, MED-004, MED-005, PF-001, PF-002, PF-003, SH-001, SH-002, SH-003, SH-004, SH-005, SH-006, SH-008, SU-001, SU-003 |
| Corroborated (both) | _none_ |
| Expected hint | SH-002 |
| Hint hit by L1 | _none_ |
| Hint hit by L2 | SH-002 |
| Hint missed by both | _none_ |

## `gilman_yellow_wallpaper` (literature)
*Source:* Charlotte Perkins Gilman, The Yellow Wallpaper

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-001, CD-006, CD-007, CD-008, HO-001, HO-005, HO-006, MED-004, PF-001, PF-002, PF-003, SH-001, SH-002, SH-003, SH-004, SU-001, SU-003 |
| Corroborated (both) | _none_ |
| Expected hint | CD-003, CD-006 |
| Hint hit by L1 | _none_ |
| Hint hit by L2 | CD-006 |
| Hint missed by both | CD-003 |

## `tolstoy_anna_karenina` (literature)
*Source:* Leo Tolstoy, Anna Karenina

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-001, HO-002, HO-005, HO-006, MED-004, SH-002, SH-004, SH-006, SH-008, SU-003 |
| Corroborated (both) | _none_ |
| Expected hint | CD-001, SH-001, SH-002 |
| Hint hit by L1 | _none_ |
| Hint hit by L2 | CD-001, SH-002 |
| Hint missed by both | SH-001 |

## `dostoevsky_crime_punishment` (literature)
*Source:* Fyodor Dostoevsky, Crime and Punishment

| Bucket | Flag IDs |
|---|---|
| L1 only | CD-001 |
| L2 only | CD-002, CD-005a, CD-005b, CD-005c, CD-005d, CD-006, CD-007, CD-008, HO-001, HO-002, HO-003, HO-005, HO-006, MED-004, PF-002, SH-004, SU-003 |
| Corroborated (both) | _none_ |
| Expected hint | CD-002, CD-005c |
| Hint hit by L1 | _none_ |
| Hint hit by L2 | CD-002, CD-005c |
| Hint missed by both | _none_ |

## `vignette_crisis_intake` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | CD-002, CD-005a, MED-001 |
| L2 only | CD-007, HO-001, HO-003, HO-006, MED-002, MED-004, MED-005, PF-003, SH-001, SH-003, SH-004, SH-006, SU-002, SU-003, SU-004 |
| Corroborated (both) | SH-002, SH-008, SU-001 |
| Expected hint | CD-002, CD-003, CD-005a, MED-002, SH-004, SH-008, SU-001, SU-003 |
| Hint hit by L1 | CD-002, CD-005a, SH-008, SU-001 |
| Hint hit by L2 | MED-002, SH-004, SH-008, SU-001, SU-003 |
| Hint missed by both | CD-003 |

## `vignette_routine_session` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-006, MED-004, PF-001, PF-002, PF-003, SH-001, SH-003, SU-001, SU-004 |
| Corroborated (both) | PF-004, PF-005 |
| Expected hint | PF-001, PF-002, PF-004, PF-005 |
| Hint hit by L1 | PF-004, PF-005 |
| Hint hit by L2 | PF-001, PF-002, PF-004, PF-005 |
| Hint missed by both | _none_ |

## `vignette_mixed_presentation` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | MED-004, PF-002, SH-003 |
| Corroborated (both) | CD-001, PF-001, SH-002 |
| Expected hint | CD-001, CD-002, PF-001, PF-002 |
| Hint hit by L1 | CD-001, PF-001 |
| Hint hit by L2 | CD-001, PF-001, PF-002 |
| Hint missed by both | CD-002 |

## `vignette_journal_entry` (clinical_vignette)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | MED-001, SH-001 |
| L2 only | CD-006, HO-006, MED-004, MED-005, PF-001, PF-002, SH-002, SH-003, SH-004, SU-003, SU-004 |
| Corroborated (both) | CD-001 |
| Expected hint | CD-001, CD-002, CD-004, MED-002, PF-001, SH-001 |
| Hint hit by L1 | CD-001, SH-001 |
| Hint hit by L2 | CD-001, PF-001 |
| Hint missed by both | CD-002, CD-004, MED-002 |

## `true_negative_weather` (true_negative)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | PF-001, PF-002, PF-003, PF-004, SU-003 |
| Corroborated (both) | _none_ |

## `true_negative_recipe` (true_negative)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-008, HO-005, MED-004, PF-001, PF-002, PF-003, SU-001, SU-003 |
| Corroborated (both) | _none_ |

## `true_negative_sports` (true_negative)
*Source:* synthetic

| Bucket | Flag IDs |
|---|---|
| L1 only | _none_ |
| L2 only | CD-008, HO-005, HO-006, MED-004, PF-001, PF-002, PF-003, SU-001, SU-003 |
| Corroborated (both) | _none_ |

## Aggregate

- L1-only flag emissions: 6
- L2-only flag emissions: 128
- Corroborated (both layers agreed): 9
- L1/L2 agreement rate: 6.3%

> Agreement rate is informational, not a quality gate. L1 and L2 are measuring different things; agreement simply indicates overlap where both layers had strong-enough signal to emit.
