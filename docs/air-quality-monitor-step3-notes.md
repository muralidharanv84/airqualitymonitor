# Step 3 - Front shell (display bezel) model

## What I built
- A parametric OpenSCAD front shell model with rounded corners, a display window cutout, three right-side button access holes (side press), and lower intake vent slots.
- Exported STL and PNG renders for visual inspection.

## Files
- OpenSCAD source: `cad/air-quality-monitor-front-shell.scad`
- STL export: `cad/air-quality-monitor-front-shell.stl`
- Render (iso): `renders/air-quality-monitor-front-shell-iso.png`
- Render (front): `renders/air-quality-monitor-front-shell-front.png`

## Key dimensions used
- Outer shell width/height: `front_shell_w`, `front_shell_h` (from TP size + bezel margin).
- Front face thickness: `face_thk = 2.0 mm`.
- Display window: `window_w`, `window_h` with `window_clear = 0.4 mm`.
- Button access: `button_count = 3`, `button_hole_d = 2.6 mm`, `button_pitch = 7.82 mm`, `button_hole_len = 4.0 mm`.
- Front vent slots: `front_vent_slot_w = 18 mm`, `front_vent_slot_h = 2 mm`, `front_vent_slot_count = 3`.

## Assumptions / placeholders (needs confirmation)
- Button offsets now use the diagram values (7.84 mm top offset from board edge, 7.82 mm pitch); horizontal offset assumes the board is centered behind the touch panel and the button center is on the board edge.
- Front shell depth `front_shell_d = 18 mm` is a starting value only; needs adjustment after standoff height and internal clearance are finalized.
- No front tilt or display recess lip yet; these need to be added for the angled housing and rear-install board design.

## Update for revised requirements
- Fuse the front display housing with the rear sensor cabinet into a single main body.
- Move the display vent to the bottom of the display area on the main body.
- Add two sensor chamber bottom vents in the main body.
- Keep the right-side button holes aligned, but ensure the board installs from the rear.
## How to preview
- Open `cad/air-quality-monitor-front-shell.scad` in OpenSCAD and render (F6) or export via CLI for snapshots.

## Step 3 completion check
- Front shell geometry is now modeled and viewable.
- Render previews generated for quick sanity checks.
