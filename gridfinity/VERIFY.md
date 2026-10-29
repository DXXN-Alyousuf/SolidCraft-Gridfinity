# VERIFY

CLI: `solidcraft-cli 0.26.0`, built from tangency-labs/solidcraft `main` (`Cargo.toml` version 0.26.0).
Evidence files are in `out/p1/`. Expected volumes are computed analytically from `SPEC.md`
(rounded-square area w^2 - (4 - pi) r^2, integrated along the 45 degree slopes).

## P1 Baseplate

### Rebuild, closure, size (`solidcraft-cli run` exit 0 means no failed timeline feature)

| Case | run exit | bodies / closed | volume measured (mm3) | expected | diff | bbox measured | bbox expected |
|------|----------|-----------------|----------------------|----------|------|---------------|---------------|
| 2x2 light | 0 | 1 / true | 5098.87 | 5099.14 | -0.005% | 84 x 84 x 4.6 | 84 x 84 x 4.6 |
| 2x2 skeleton | 0 | 1 / true | 28207.85 | 28207.81 | +0.000% | 84 x 84 x 8.6 | 84 x 84 x 8.6 |
| 2x2 full | 0 | 1 / true | 33268.20 | 33268.20 | 0.000% | 84 x 84 x 8.6 | 84 x 84 x 8.6 |
| 3x4 light | 0 | 1 / true | 15425.19 | 15423.78 | +0.009% | 126 x 168 x 4.6 | 126 x 168 x 4.6 |

2x2 and 3x4 differ by `--nx/--ny` only. Types differ measurably: light 5098.87, skeleton 28207.85,
full 33268.20 mm3 (ordering not assumed; measured).

### Option toggles (2x2, all run exit 0, all closed, bbox 84 x 84 x 8.6)

| Case | volume measured | expected | cylinder faces (baseline full: 20) |
|------|-----------------|----------|-----------------------------------|
| full + magnets | 31994.11 | 33268.20 - 16 x pi x 3.25^2 x 2.4 = 31994.0 | 36 (+16) |
| full + screws | 32815.92 | 33268.20 - 16 x pi x 1.5^2 x 4 = 32815.8 | 36 (+16) |
| full + magnets + screws | 31813.20 | 31994.0 - 16 x pi x 1.5^2 x 1.6 = 31812.9 | 52 (+32) |
| skeleton + magnets + screws + connection holes | 25209.04 | 25208.47 (+0.002%) | 80 |

Hole count: 4 per cell x 4 cells = 16 each of magnet and screw (face-count delta +16 each).

### Hole positions and sizes (`inspect.measure` on the face, full + magnets + screws)

Centres measured exactly at the expected (x, y); magnet face z = 2.8, screw face z = 0.8:

| Expected (x, y) | magnet centre / dia | screw centre / dia |
|-----------------|--------------------|--------------------|
| (8, 8) | (8.000, 8.000) / 6.500 | (8.000, 8.000) / 3.000 |
| (34, 8) | (34.000, 8.000) / 6.500 | (34.000, 8.000) / 3.000 |
| (8, 34) | (8.000, 34.000) / 6.500 | (8.000, 34.000) / 3.000 |
| (34, 34) | (34.000, 34.000) / 6.500 | (34.000, 34.000) / 3.000 |
| (50, 8) | (50.000, 8.000) / 6.500 | (50.000, 8.000) / 3.000 |
| (76, 76) | (76.000, 76.000) / 6.500 | (76.000, 76.000) / 3.000 |

This proves the generator puts holes where it says. It does not prove the 8.0 mm offset itself
(derived from the spec drawing, ~85% sure; see `SPEC.md`).

### Exports and snapshots

`out/p1/<case>.step`, `.stl`, `.3mf`, `.png` exist for every case above and for the three option
cases. 3MF and STL come from `solidcraft-cli run --out` (format chosen by extension).
Visual check: `out/p1/bp_2x2_skeleton.png` shows four cells with 45 degree slopes and a window in each floor.

### Failures found on the way (and what changed)

1. Cutting the spec profile exactly failed: zero-width top edge, coincident faces. Fix: `--top-trim`.
2. Cutting the cone and vertical pieces one after another failed on a 2x1 plate. Fix: join them first.
3. Lofting one cutter was rejected: spline faces, volume 6671.6 vs exact 6911.1 mm3 (3.5% low).
4. Joining the skeleton window with the pocket pieces failed. Fix: cut the window separately first.

P1 status: PASS for the cases above. Not run: 3x4 skeleton/full, hole options at 3x4.
