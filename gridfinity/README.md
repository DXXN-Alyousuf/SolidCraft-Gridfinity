# gridfinity-solidcraft

Gridfinity baseplate and bin generator for SolidCraft (v0.26.0). Delivered as a script generator:
a Python 3 CLI (standard library only) that writes a SolidCraft command script (JSON) and can run
`solidcraft-cli` to export STEP, STL, 3MF and an iso PNG.

Status: **P1 baseplate done. P2 to P5 not built yet.** Dimensions and sources: `SPEC.md`.
Evidence: `VERIFY.md`. Physical fit is unverified until test-printed.

## Run

```sh
python3 p1_baseplate.py --nx 2 --ny 2 --type full --magnets --screws \
    --script out/bp.json --run out/bp --cli /path/to/solidcraft-cli
```

`--script` writes the JSON script. `--run BASENAME` also runs `solidcraft-cli` and writes
`BASENAME.step`, `.stl`, `.3mf`, `.png`. Without `--run`, replay it yourself:
`solidcraft-cli run out/bp.json --out out/bp.step --out out/bp.stl --out out/bp.3mf`.

## Baseplate options (p1_baseplate.py)

| Option | Default | Meaning |
|--------|---------|---------|
| `--nx`, `--ny` | 2, 2 | cells along X and Y |
| `--pitch` | 42 | cell size, mm |
| `--type` | light | `light`: profile frame only, cells open through the bottom. `full`: solid thick plate under the profile. `skeleton`: thick plate with a window cut in each cell |
| `--plate-thickness` | 4.0 | thick plate under the profile (skeleton, full), mm. Not from the spec |
| `--skeleton-margin` | 12.0 | window inset from the cell edge, mm. Not from the spec; must stay above hole offset + magnet radius (11.25) |
| `--skeleton-radius` | 3.0 | window corner radius, mm. Not from the spec |
| `--magnets` | off | magnet pockets at the four corners of each cell (skeleton, full) |
| `--magnet-diameter` | 6.5 | pocket diameter, mm (spec drawing, for a 6 mm magnet) |
| `--magnet-depth` | 2.4 | pocket depth, mm (2 mm magnet + 0.4; not from the spec) |
| `--screws` | off | screw holes at the four corners of each cell (skeleton, full) |
| `--screw-diameter` | 3.0 | mm (M3, spec) |
| `--hole-offset` | 8.0 | hole centre from the cell edge, mm (derived from the spec drawing) |
| `--connection-holes` | off | skeleton only: holes along X and Y through the plate, mid-cell |
| `--connection-diameter` | 3.2 | mm. Not from the spec |
| `--top-trim` | 0.05 | see deviations |
| `--script` | required | output JSON path |
| `--run` | off | basename for STEP/STL/3MF/PNG exports |
| `--cli` | solidcraft-cli | path to the CLI |

Magnets, screws and connection holes are rejected with `--type light` (no plate to put them in).

## Deviations from the spec

- **Top trim.** The spec profile has a vertical outer wall and a 45 degree slope that meet in a
  zero-width edge at the top. The kernel cannot cut that (boolean "coincident faces" error), so the
  profile top is trimmed by `--top-trim` (0.05 mm): the baseplate is 4.60 mm tall instead of 4.65 and
  every rim has a 0.1 mm flat. Set `--top-trim 0` to get the spec height; expect the cut to fail.
- **Corner radii inside the pocket** (1.15 at the bottom, 1.85 at the vertical section) are derived
  by offsetting the 4.0 mm outer radius, the same pattern the spec shows for the bin. Not read from a drawing.

## Known limits

- Larger plates are slow: the kernel panics internally and retries on a 3x4 plate, about 4 minutes
  per replay (run, snapshot and eval each replay the script). 2x2 takes about 30 s.
- The `skeleton` window and the connection holes are my interpretation of the add-in's feature names.
- Only `light` was run at 3x4. `skeleton`, `full` and the hole options were run at 2x2.
- The cutter pieces are joined before each cut. Cutting them one after another fails on a plate
  larger than one cell (kernel limit).

## Licence notes

- **Gridfinity** is by Zack Freedman and licensed CC BY-NC-SA. The dimensions in `SPEC.md` come from
  the willtree8 Gridfinity Design Reference (same licence), gridfinity.xyz and Stu142's documentation.
  Anything derived from them should be shared under the same terms and not used commercially.
- **Fusion add-in** (github.com/Le0Michine/FusionGridfinityGenerator, CC BY-NC-SA 4.0): only its README
  was read, for option names and the feature list. No source code was read, copied or paraphrased. This
  project does not reuse its name.
- This project's own licence is not chosen yet. Decide before publishing.
