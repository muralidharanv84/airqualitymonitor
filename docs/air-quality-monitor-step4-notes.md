# Step 4 - Display dev board mounting + USB clearance

## What I built
- Added four M2.5 standoffs at the display dev board mounting hole locations (41.00 mm × 60.00 mm spacing), centered to the front shell.
- Added a bottom USB Type-C clearance slot centered on the shell.

## Files (updated)
- OpenSCAD source: `cad/air-quality-monitor-front-shell.scad`
- STL export: `cad/air-quality-monitor-front-shell.stl`
- Render (iso): `renders/air-quality-monitor-front-shell-iso.png`
- Render (front): `renders/air-quality-monitor-front-shell-front.png`

## Key parameters used
- Standoff height: `standoff_h = 4.0 mm` (derived from 6.0 mm front-to-PCB-back ref and 2.0 mm face thickness).
- Screw size: `screw_d = 2.5 mm` (M2.5) with `screw_clear_d = 2.7 mm`.
- Mount hole spacing: `mount_hole_spacing_x = 41.00 mm`, `mount_hole_spacing_y = 60.00 mm`.
- USB cutout: `usb_cut_w = 10.0 mm`, `usb_cut_h = 4.0 mm`, `usb_cut_d = 12.0 mm`.

## Assumptions / placeholders (needs confirmation)
- USB slot position is centered; confirm actual port offset before finalizing the opening.
- Cable strain relief is represented by the deeper slot only; we can add a more specific channel once the board is test-fit.

## Update for revised requirements
- Move the display board standoffs to the display rear cover so the board mounts to the lid with M2.5 screws.
- Replace the bottom USB-C clearance with a rear USB-C opening on the sensor slide-in door (via extension cable).
- Add a LiPo battery recess and a top vent to the display rear cover.

## Step 4 completion check
- Standoffs align with the published mounting hole spacing.
- USB clearance slot exists at the bottom edge for a downward cable.
