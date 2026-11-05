"""Sheet grid zones: which border zone ("G-6") a point or box on a drawing falls in. Stdlib only.

    python scripts/sheet_zone.py 449.5 153.0 --frame 9.4,19.5,857.1,981.1        # -> G-6 (OPEN100 sheet 0)

One convention, shared by every tool that writes a zone (one_map.py sheet-from-prediction, generate.py's review
queue column `zone_on_sheet`), and the same rule scripts/draw_pid_from_model.py uses to letter its generated sheets:

- the grid spans the drawing FRAME (the inner border rectangle), in the same units as the point; for a reader's
  0-1000 boxes the default frame is the whole image (0, 0, 1000, 1000);
- the default grid is 8 rows x 12 columns, as printed on the OPEN100 sheets and on the generated TE sheets;
- origin "bottom-right" (default; ASME Y14.1 style, as those borders print it): rows are lettered A at the BOTTOM up
  to H at the top, columns numbered 1 at the RIGHT up to 12 at the left. Origin "top-left" (ISO 5457 style): A at
  the top, 1 at the left;
- a zone is written ROW-COL ("G-6"), the form build_twin.GRID_REF reads off off-page flags;
- a box is zoned by its centre; a point outside the frame is clamped to the nearest edge zone (as the generator does).

A zone computed over the whole image when the sheet's printed border sits inside it (a margin, a title block beside
the frame) can be off by a row or column near the edges; pass the sheet's frame for zones that match its border.
"""
import argparse
import sys

ORIGINS = ("bottom-right", "top-left")
DEFAULT_ROWS, DEFAULT_COLS = 8, 12
WHOLE_SHEET = (0.0, 0.0, 1000.0, 1000.0)
ROW_LETTERS = "ABCDEFGHJKLMNPRSTUVWXYZ"  # I, O and Q are skipped on drawing borders


def zone_at(x, y, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, frame=WHOLE_SHEET, origin="bottom-right"):
    """Zone of point (x, y) on a grid of rows x cols over frame (x0, y0, x1, y1); y grows downward."""
    if origin not in ORIGINS:
        raise ValueError(f"zone origin must be one of {', '.join(ORIGINS)} (got {origin!r})")
    if not (isinstance(rows, int) and isinstance(cols, int) and 1 <= rows <= len(ROW_LETTERS) and 1 <= cols <= 99):
        raise ValueError(f"zone grid needs 1-{len(ROW_LETTERS)} rows and 1-99 columns (got {rows}x{cols})")
    fx0, fy0, fx1, fy1 = frame
    if not (fx1 > fx0 and fy1 > fy0):
        raise ValueError(f"zone frame {frame} is empty or reversed")
    ci = min(cols - 1, max(0, int((x - fx0) / ((fx1 - fx0) / cols))))  # 0 = leftmost column
    ri = min(rows - 1, max(0, int((y - fy0) / ((fy1 - fy0) / rows))))  # 0 = top row
    if origin == "bottom-right":
        return f"{ROW_LETTERS[rows - 1 - ri]}-{cols - ci}"
    return f"{ROW_LETTERS[ri]}-{ci + 1}"


def zone_of_box(box, **grid):
    """Zone of a box [x0, y0, x1, y1] by its centre; None for a missing or malformed box."""
    if not (isinstance(box, (list, tuple)) and len(box) == 4
            and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in box)):
        return None
    return zone_at((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, **grid)


def parse_grid(text):
    """'8x12' -> (8, 12): rows x columns."""
    try:
        r, c = (int(v) for v in str(text).lower().split("x"))
    except ValueError:
        raise ValueError(f"zone grid must be ROWSxCOLS such as 8x12 (got {text!r})") from None
    zone_at(0, 0, r, c)  # validates the size
    return r, c


def parse_frame(text):
    """'x0,y0,x1,y1' -> a frame tuple."""
    try:
        f = tuple(float(v) for v in str(text).split(","))
    except ValueError:
        f = ()
    if len(f) != 4:
        raise ValueError(f"zone frame must be x0,y0,x1,y1 (got {text!r})")
    zone_at(f[0], f[1], frame=f)  # validates the frame
    return f


def grid_record(rows=DEFAULT_ROWS, cols=DEFAULT_COLS, frame=WHOLE_SHEET, origin="bottom-right"):
    """The convention as data, written next to every zone so a reader of the output can check it."""
    return {"rows": rows, "cols": cols, "origin": origin, "frame_0_1000": list(frame), "format": "ROW-COL",
            "rule": ("rows lettered A at the bottom, columns numbered 1 at the right (ASME Y14.1 style)"
                     if origin == "bottom-right" else
                     "rows lettered A at the top, columns numbered 1 at the left (ISO 5457 style)")
            + "; a box is zoned by its centre"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("x", type=float)
    ap.add_argument("y", type=float)
    ap.add_argument("--grid", default=f"{DEFAULT_ROWS}x{DEFAULT_COLS}", help="ROWSxCOLS (default 8x12)")
    ap.add_argument("--frame", default=",".join(str(v) for v in WHOLE_SHEET), help="x0,y0,x1,y1 (default whole sheet)")
    ap.add_argument("--origin", choices=ORIGINS, default="bottom-right")
    a = ap.parse_args(argv)
    try:
        rows, cols = parse_grid(a.grid)
        print(zone_at(a.x, a.y, rows, cols, parse_frame(a.frame), a.origin))
    except ValueError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
