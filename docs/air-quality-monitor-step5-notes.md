# Step 5 - Rear case + sensor chambers

## What I built
- A rear shell with matching outer profile to the front shell and an internal divider to create two front/back sensor chambers.
- No venting on the rear wall yet (per the plan to do vent slots on the removable lid as the final step).

## Files
- OpenSCAD source: `cad/air-quality-monitor-rear-shell.scad`
- STL export: `cad/air-quality-monitor-rear-shell.stl`
- Render (iso): `renders/air-quality-monitor-rear-shell-iso.png`
- Render (front): `renders/air-quality-monitor-rear-shell-front.png`
- Render (back): `renders/air-quality-monitor-rear-shell-back.png`
- Render (side): `renders/air-quality-monitor-rear-shell-side.png`
- Render (top): `renders/air-quality-monitor-rear-shell-top.png`

## Key parameters used
- Rear shell depth: `rear_shell_d = 26.0 mm` (tunable).
- Divider thickness: `divider_thk = 2.0 mm`.
- Front chamber depth: `front_chamber_d = 12.0 mm` (rear chamber = remainder).

## Assumptions / placeholders (needs confirmation)
- Slide-in rear wall rails and detents are deferred to Step 7 (assembly features).
- Sensor mounting shelves and final chamber sizing will be refined after test fitting SPS30/SCD40.
- Vent slots are intentionally deferred to the final step.

## Update for revised requirements
- Fuse the front display housing and rear sensor cabinet into a single main body.
- Split the rear into two components: display rear cover and sensor slide-in door.
- Add a USB-C opening to the sensor door (vents later).
- Add two bottom vents on the main body for the sensor chamber.

## Step 5 completion check
- Rear shell aligns in outer size with the front shell.
- Divider wall isolates two chambers along depth.
