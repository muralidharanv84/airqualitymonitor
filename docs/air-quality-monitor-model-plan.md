# Air Quality Monitor 3D Model Plan

## Goal
Create a parametric, printable 3D enclosure inspired by the Qingping Air Monitor 2. The front face must fit flush with the Waveshare 2.8" ESP-32 LCD (USB port down), expose three small button holes on the right, include a rear battery insert (2500 mAh) with screw bosses/inserts, and mount SPS30 + SPS40 sensor boards on the back with proper air flow separation.

## Technical approach (format + tooling)
- **Primary CAD tool:** Autodesk Fusion 360 (parametric timeline + user parameters). The **master file** will be saved as `.f3d` so it remains fully editable in Fusion 360.
- **Exchange formats:** export `.step` for interoperability and archival, plus `.stl`/`.3mf` per-part for printing.
- **Model structure:** separate components for front shell, rear shell, battery insert, and sensor mounts; assemble in a top-level assembly to preserve parametric constraints.
- **Parameter control:** use Fusion 360 **Change Parameters** table for all key dimensions; name parameters clearly (e.g., `wall_thk`, `lcd_window_w`, `button_pitch`).
- **Optional automation:** Fusion 360’s built-in Python API can be used to regenerate derived exports. No third-party CAD libraries are required if modeling directly in Fusion 360.

## Render + image workflow
- **Primary render:** Fusion 360 Render workspace for photorealistic images; capture isometric and sectioned views per step.
- **Quick checks:** Fusion 360 “Capture Image” for fast progress screenshots.
- **Optional external render:** export STEP and use Blender (or FreeCAD + Blender) if higher quality or custom lighting is needed.

## Required assets
- `docs/Waveshare ESP32-S3 Touch LCD 2.8 2D diagram.png` (2D dimensions).
- `docs/esp32-s3-touch-lcd-2_8.stp` (3D reference for fit and clearance).
- Datasheets or measured dimensions for SPS30, SPS40 dev board, and 2500 mAh battery.

## Step-by-step plan (render/check at each step)

1. **Collect reference dimensions**
   - Measure the Waveshare 2.8" ESP-32 LCD (use `docs/Waveshare ESP32-S3 Touch LCD 2.8 2D diagram.png` + `docs/esp32-s3-touch-lcd-2_8.stp`).
   - Identify: outer PCB footprint, display active area, button locations (right side), USB port position (bottom), mounting holes, and keepout areas.
   - Collect SPS30 + SPS40 dev board dimensions and airflow inlet/outlet locations.
   - Measure 2500 mAh battery size (length/width/thickness) and connector clearance.
   - **Render/check:** create a basic bounding-box scene with all components in a single assembly to validate clearances.

2. **Define global parameters**
   - Set key parameters (in the Fusion 360 **Change Parameters** table): wall thickness, front bezel margin, corner radius, front angle, standoff heights, sensor bay spacing, screw boss diameter, insert size, vent slot size/pitch.
   - **Render/check:** confirm parameter table updates the placeholder shell dimensions and that parameter names match expected features.

3. **Model the front shell (display bezel)**
   - Create the main front enclosure volume with rounded corners, inspired by Qingping proportions.
   - Cut the display window opening so the Waveshare display sits flush.
   - Add three button holes on the right aligned to the board buttons; include chamfers for easy pressing.
   - Add a lower front vent slot (or multiple) for air intake similar to Qingping.
   - **Render/check:** verify the display aligns flush and buttons are accessible without interference.

4. **Add internal mounting for the display dev board**
   - Add board standoffs aligned with mounting holes.
   - Create cable routing channels, especially for USB (bottom-facing).
   - Add clearance for the USB connector and cable strain relief in the bottom.
   - **Render/check:** fit the board in place and ensure the USB cable can route downward.

5. **Design rear case and sensor chambers**
   - Create a rear housing that mates with the front shell (snap features or screws).
   - Split the internal volume into two sensor zones (SPS30 and SPS40) with isolation walls to reduce cross-contamination.
   - Add venting for each sensor chamber (inlet/outlet grills or slots), ensuring air circulation paths.
   - **Render/check:** verify separate airflow paths and no collision with board standoffs.

6. **Battery insert and mounting system**
   - Design a battery tray insert sized for the 2500 mAh battery.
   - Add screw bosses and insert locations to fasten the tray to the display dev board.
   - Provide wiring clearance and a service loop path.
   - **Render/check:** insert fits and screws align; no interference with sensors.

7. **Assembly features**
   - Add perimeter screw bosses or snap-fit tabs for front-to-back assembly.
   - Include alignment pins/keys for repeatable assembly.
   - Add gasket/foam channel options around the display window if desired for dust/light sealing.
   - **Render/check:** assemble front/back shells and inspect for gaps or clashes.

8. **Printability and serviceability adjustments**
   - Ensure overhangs are printable; add fillets/chamfers where needed.
   - Split parts if needed for print orientation.
   - Verify screw access and sensor replacement access.
   - **Render/check:** simulate print orientation and confirm minimal support need.

9. **Final validation**
   - Check overall proportions vs. Qingping inspiration.
   - Verify USB port orientation (down) and button access.
   - Confirm air paths are unobstructed and sensor isolation is preserved.
   - **Render/check:** final assembled render with transparency to show internals.

## Deliverables
- `air-quality-monitor.f3d` (master parametric model for Fusion 360).
- `air-quality-monitor.step` (assembly export).
- Per-part print files: `.stl` or `.3mf` for front shell, rear shell, battery insert, and sensor mounts.
- Rendered images from Fusion 360 (isometric + section cut views).

## Iteration notes
- After each step, record measurements, changes, and rendering screenshots for review.
- Iterate parameters if any clearance issues appear.
- Keep the design parametric so board or battery changes are low effort.
