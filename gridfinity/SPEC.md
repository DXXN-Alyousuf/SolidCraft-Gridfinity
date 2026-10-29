# Gridfinity dimensions used by gridfinity-solidcraft

All values in mm. Nothing here comes from memory. Every row cites a source.

## Sources

| ID | Source | How read |
|----|--------|----------|
| S1 | "Gridfinity Design Reference v5", graphic by willtree8, based on Zack Freedman's designs. The same graphic family is embedded on https://gridfinity.xyz/specification/ as `spec_draft_willtree8.jpg` (page itself marks the spec "work in progress"). | Image supplied by the user in this session; values read by eye, then cross-checked by arithmetic (see Checks). |
| S2 | https://gridfinity.xyz/specification/ | Fetched via Firecrawl: magnets 6 mm dia x 2 mm thick, M3 screws in the corners. |
| S3 | https://github.com/Stu142/Gridfinity-Documentation ("Original Spec", Zack's models) | README fetched; baseplate PDF text extracted. Drawings are SVGs and were not readable. Used only as a cross-check. |

## Grid and bin footprint

| Quantity | Value | Source |
|----------|-------|--------|
| Cell pitch (baseplate cell, bin unit) | 42 | S1 |
| Bin footprint per unit | 41.5 (42 - 2 x 0.25 tolerance) | S1 |
| Height unit | 7 | S1 |
| Height rule | Bin height n u = n x 7, base included in the count. Stacking lip adds ~4.4 on top (2u = 14 + 4.4 = 18.4). | S1 |

## Bin base (foot) profile, bottom up

| Segment | Value | Source |
|---------|-------|--------|
| Bottom chamfer 45 deg | 0.8 | S1 |
| Vertical | 1.8 | S1 |
| Top chamfer 45 deg | 2.15 | S1 |
| Foot height total | 4.75 | S1 (sum checked) |
| Flat bottom width, 1 unit | 35.6 | S1 (checked) |
| Outer corner radius (plan) | 3.75 (shown as 7.5 dia) | S1 |
| Corner radius after 2.15 inset | 1.6 (3.2 dia) | S1 (checked) |
| Corner radius after 2.95 inset | 0.8 (1.6 dia) | S1 (checked) |

## Baseplate profile

| Quantity | Value | Source |
|----------|-------|--------|
| Cell | 42 x 42 | S1, S3 |
| Profile segments (45 deg, vertical, 45 deg) | 0.7 / 1.8 / 2.15 | S1 |
| Profile height | 4.65 (S1 labels it "~5") | S1 (sum checked) |
| Corner radius | 4.0 (8.0 dia) | S1 (checked = 3.75 + 0.25) |
| Inner opening per cell | 37.7 (42 - 2 x 2.15) | S3 (checked) |

## Stacking lip profile

| Segment | Value | Source |
|---------|-------|--------|
| 45 deg | 0.7 | S1 |
| Vertical | 1.8 | S1 |
| 45 deg | 1.9 | S1 |
| Lip height total | ~4.4 | S1 (sum checked) |
| Offset between lip and mating baseplate | 0.25 | S1 |

## Holes

| Quantity | Value | Source |
|----------|-------|--------|
| Magnet | 6 dia x 2 thick | S2, S3 |
| Magnet pocket drawn in plan | 6.5 dia | S1 |
| Screw hole drawn in plan | 3.0 dia (M3) | S1, S2 |
| Heat-set insert hole (optional) | 4.2 dia | S3 |
| Hole centre from cell edge | 8.0 (= 0.25 + 2.15 + 0.8 + 4.8) | S1, derived. ~85% sure the 4.8 dimension runs from the 0.8 step to the hole centre; confirm against the built model. |

## Not in any source (user parameters, not spec)

Wall thickness, floor thickness, magnet and screw pocket depth, label tab size and angle, scoop radius, lip notches, compartment dividers, PCB pocket. These are named generator options, not spec dimensions.

## Checks (run in this session)

- 0.8 + 1.8 + 2.15 = 4.75, 0.7 + 1.8 + 1.9 = 4.4, 0.7 + 1.8 + 2.15 = 4.65: match S1.
- 42 - 2 x 0.25 = 41.5; 41.5 - 2 x (2.15 + 0.8) = 35.6: match S1.
- 3.75 - 2.15 = 1.6 and 3.75 - 2.95 = 0.8 (dia 3.2 and 1.6): match S1. 3.75 + 0.25 = 4.0 (dia 8.0): matches S1.

## Discrepancies

1. S3 baseplate PDF prints "42 - 2.85 - 2.85 = 36.6". Arithmetic gives 36.3. The PDF also shows 36.3. S1 and the arithmetic win: 36.3.
2. Community note (https://www.reddit.com/r/gridfinity/comments/1gdupij/): stacking bins do not come out to a consistent height because lip (4.4) differs from foot (4.75) by 0.35. Not applied. Generator follows S1 and states the 0.35 mismatch in README.
3. Other generators use different lip heights and radii. Not used.

## Licence

Gridfinity is by Zack Freedman. S1 is marked CC BY-NC-SA. Output geometry is derived from these dimensions; the project README must carry the notice and the user must decide how to licence results.
