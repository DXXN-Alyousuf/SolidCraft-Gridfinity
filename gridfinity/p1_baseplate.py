#!/usr/bin/env python3
"""gridfinity-solidcraft, phase 1: baseplate command-script generator.

Writes a SolidCraft command script (JSON). Dimensions come from SPEC.md.
Every option is a CLI flag; defaults are listed in README.md.
"""
import argparse
import json
import subprocess
import sys

# Spec profile (SPEC.md, baseplate): 45deg / vertical / 45deg
PROFILE_BOTTOM = 0.7    # bottom chamfer height (and width)
PROFILE_VERT = 1.8
PROFILE_TOP = 2.15      # top chamfer height (and width)
CORNER_R = 4.0          # outer corner radius at the top opening (8.0 dia)


class Script:
    def __init__(self):
        self.commands = []

    def add(self, command, **params):
        self.commands.append({"command": command, "params": params})

    def rounded_sketch(self, z, x0, y0, x1, y1, radius):
        self.add("sketch.create", plane="XY", offset=z)
        self.add("sketch.rectangle.rounded", p0=[x0, y0], p1=[x1, y1], radius=radius)
        self.add("sketch.finish")

    def extrude(self, distance, name, operation="new", taper=None):
        params = {"distance": distance, "operation": operation, "body_name": name}
        if taper is not None:
            params["taper"] = f"{taper} deg"
        self.add("solid.extrude", **params)


def build(o):
    """Return the command list for a baseplate with options namespace `o`."""
    s = Script()
    p = o.pitch
    thick = o.type != "light"
    t = o.plate_thickness if thick else 0.0
    total_h = t + PROFILE_BOTTOM + PROFILE_VERT + PROFILE_TOP - o.top_trim
    w, h = o.nx * p, o.ny * p

    s.rounded_sketch(0, 0, 0, w, h, CORNER_R)
    s.extrude(round(total_h, 6), "Baseplate")

    # per-cell pocket: widths from the spec profile, centred in the cell
    bot_w = p - 2 * (PROFILE_TOP + PROFILE_BOTTOM)   # 36.3 at pocket bottom
    mid_w = p - 2 * PROFILE_TOP                      # 37.7 vertical section
    r_bot = CORNER_R - PROFILE_TOP - PROFILE_BOTTOM
    r_mid = CORNER_R - PROFILE_TOP
    for i in range(o.nx):
        for j in range(o.ny):
            cx, cy = i * p, j * p
            tools = []
            tag = f"C{i}_{j}"

            def sq(z, width, radius, name, dist, taper=None):
                m = (p - width) / 2
                s.rounded_sketch(z, cx + m, cy + m, cx + p - m, cy + p - m, radius)
                s.extrude(round(dist, 6), name, taper=taper)
                tools.append(name)

            if not thick:  # light: cell is open through the bottom
                sq(-1.0, bot_w, r_bot, f"{tag}A", 1.0)
            sq(t, bot_w, r_bot, f"{tag}B", PROFILE_BOTTOM, taper=45)
            sq(t + PROFILE_BOTTOM, mid_w, r_mid, f"{tag}C", PROFILE_VERT)
            # top chamfer runs 1 mm past the plate top so the cut leaves no coplanar face
            sq(t + PROFILE_BOTTOM + PROFILE_VERT, mid_w, r_mid, f"{tag}D",
               PROFILE_TOP + 1.0, taper=45)
            if o.type == "skeleton":
                m = o.skeleton_margin
                s.rounded_sketch(-1.0, cx + m, cy + m, cx + p - m, cy + p - m, o.skeleton_radius)
                s.extrude(round(t + 1.3, 6), f"{tag}W")
                s.add("solid.combine", target="Baseplate", tools=[f"{tag}W"], operation="cut")
            # joining the pieces first: cutting them one after another fails where the
            # cone and the vertical section share a rim (kernel limit, see README)
            s.add("solid.combine", target=tools[-1], tools=tools[:-1], operation="join")
            s.add("solid.combine", target="Baseplate", tools=[tools[-1]], operation="cut")
            if o.magnets or o.screws:
                holes = []
                for k, (hx, hy) in enumerate([(o.hole_offset, o.hole_offset),
                                              (p - o.hole_offset, o.hole_offset),
                                              (o.hole_offset, p - o.hole_offset),
                                              (p - o.hole_offset, p - o.hole_offset)]):
                    if o.magnets:   # pocket from the plate top surface down
                        s.add("solid.cylinder", diameter=o.magnet_diameter,
                              height=round(o.magnet_depth + 0.5, 6),
                              base=[cx + hx, cy + hy, round(t - o.magnet_depth, 6)],
                              operation="new", body_name=f"{tag}M{k}")
                        holes.append(f"{tag}M{k}")
                    if o.screws:    # through the whole plate; top 0.8 above the plate top
                        s.add("solid.cylinder", diameter=o.screw_diameter,
                              height=round(t + 1.8, 6), base=[cx + hx, cy + hy, -1.0],
                              operation="new", body_name=f"{tag}S{k}")
                        holes.append(f"{tag}S{k}")
                if len(holes) > 1:
                    s.add("solid.combine", target=holes[-1], tools=holes[:-1], operation="join")
                s.add("solid.combine", target="Baseplate", tools=[holes[-1]], operation="cut")
    if o.connection_holes:   # pin / screw holes along X and Y through the plate, mid-cell
        zc = round(t / 2, 6)
        for j in range(o.ny):
            s.add("solid.cylinder", diameter=o.connection_diameter, height=w + 2,
                  base=[-1.0, j * p + p / 2, zc], axis="X", operation="new", body_name=f"CX{j}")
            s.add("solid.combine", target="Baseplate", tools=[f"CX{j}"], operation="cut")
        for i in range(o.nx):
            s.add("solid.cylinder", diameter=o.connection_diameter, height=h + 2,
                  base=[i * p + p / 2, -1.0, zc], axis="Y", operation="new", body_name=f"CY{i}")
            s.add("solid.combine", target="Baseplate", tools=[f"CY{i}"], operation="cut")
    return s.commands


def main(argv=None):
    a = argparse.ArgumentParser(description="Generate a Gridfinity baseplate SolidCraft script.")
    a.add_argument("--nx", type=int, default=2, help="cells along X (default 2)")
    a.add_argument("--ny", type=int, default=2, help="cells along Y (default 2)")
    a.add_argument("--pitch", type=float, default=42.0, help="cell size mm (default 42)")
    a.add_argument("--type", choices=["light", "skeleton", "full"], default="light",
                   help="light: profile frame only; full: solid thick plate; "
                        "skeleton: thick plate with a window cut in each cell (default light)")
    a.add_argument("--plate-thickness", type=float, default=4.0,
                   help="thick plate under the profile, skeleton/full only, mm (default 4.0)")
    a.add_argument("--skeleton-margin", type=float, default=12.0,
                   help="skeleton window inset from the cell edge, mm (default 12.0)")
    a.add_argument("--skeleton-radius", type=float, default=3.0,
                   help="skeleton window corner radius, mm (default 3.0)")
    a.add_argument("--top-trim", type=float, default=0.05,
                   help="mm trimmed off the profile top so the rim has a 2*trim flat "
                        "instead of a zero-width edge the kernel cannot cut (default 0.05)")
    a.add_argument("--magnets", action="store_true",
                   help="magnet sockets at the four corners of each cell (skeleton/full only)")
    a.add_argument("--magnet-diameter", type=float, default=6.5,
                   help="magnet pocket diameter mm; spec drawing 6.5 for a 6 mm magnet (default 6.5)")
    a.add_argument("--magnet-depth", type=float, default=2.4,
                   help="magnet pocket depth mm; 2 mm magnet + 0.4, not from the spec (default 2.4)")
    a.add_argument("--screws", action="store_true",
                   help="screw holes at the four corners of each cell (skeleton/full only)")
    a.add_argument("--screw-diameter", type=float, default=3.0,
                   help="screw hole diameter mm; M3 per spec (default 3.0)")
    a.add_argument("--hole-offset", type=float, default=8.0,
                   help="hole centre distance from the cell edge mm (default 8.0)")
    a.add_argument("--connection-holes", action="store_true",
                   help="skeleton only: holes along X and Y through the plate mid-cell")
    a.add_argument("--connection-diameter", type=float, default=3.2,
                   help="connection hole diameter mm, not from the spec (default 3.2)")
    a.add_argument("--script", required=True, help="path to write the JSON script")
    a.add_argument("--run", metavar="BASENAME",
                   help="also run solidcraft-cli: writes BASENAME.step/.stl/.3mf/.png")
    a.add_argument("--cli", default="solidcraft-cli", help="path to solidcraft-cli")
    o = a.parse_args(argv)
    if o.type == "light" and (o.magnets or o.screws or o.connection_holes):
        a.error("magnets, screws and connection holes need a plate: use --type skeleton or full")
    if o.connection_holes and o.type != "skeleton":
        a.error("--connection-holes is for --type skeleton")

    with open(o.script, "w") as f:
        json.dump({"commands": build(o)}, f, indent=1)
    print(f"wrote {o.script}")
    if o.run:
        run = [o.cli, "run", o.script, "--out", o.run + ".step",
               "--out", o.run + ".stl", "--out", o.run + ".3mf"]
        if subprocess.call(run) != 0:
            return 1
        return subprocess.call([o.cli, "snapshot", o.script, "--out", o.run + ".png"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
