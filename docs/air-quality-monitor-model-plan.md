# Air Quality Monitor 3D Model Plan

## Goal
Create a parametric, printable 3D enclosure inspired by the Qingping Air Monitor 2. Requirements:

- Angled front housing for the display board.
- Display board installs from the rear; M2.5 screws secure it to the display rear cover.
- Display rear cover includes a recessed pocket for the LiPo battery.
- Three right-side button access holes aligned to the board buttons.
- Rear sensor cabinet houses the SPS30 and the SCD40 board plus a USB-C extension port.
- Rear sensor cover is a slide-in door with a USB-C opening (vents later).
- Front display housing + rear sensor cabinet are a fused main component.
- Separate rear components: display rear cover and sensor rear cover.
- Vents:
  - Main body: one vent at the bottom of the display area.
  - Main body: two vents at the bottom of the sensor chamber.
  - Display rear cover: one vent near the top.

## Technical approach (OpenSCAD)
- **Primary CAD tool:** OpenSCAD. Each component is modeled as a parameterized module in `cad/`.
- **Parameter control:** define key dimensions at the top of each `.scad` file and optionally centralize shared values in `cad/params.scad` (or a shared include).
- **Model structure:**
  - `air-quality-monitor-main-body.scad` for the fused front display housing + rear sensor cabinet.
  - `air-quality-monitor-display-cover.scad` for the display rear cover with board mounting and battery recess.
  - `air-quality-monitor-sensor-cover.scad` for the slide-in sensor door with USB-C opening.
- **Exports:** use the OpenSCAD CLI to export STLs and PNG renders; keep STLs in `cad/` and renders in `renders/`.

## Render + image workflow (multi-angle per step)
- Render from several angles before moving to the next step: at minimum iso, front, right, back, and top.
- Use consistent camera presets so changes are easy to compare.
- Example commands (adjust filenames and camera values per part):
  - `openscad -o cad/air-quality-monitor-main-body.stl cad/air-quality-monitor-main-body.scad`
  - `openscad -o renders/main-body-iso.png --imgsize=1600,1200 --camera=35,30,400,55,0,25 cad/air-quality-monitor-main-body.scad`
  - Repeat for front/right/back/top and for each component.

## Required assets
- `docs/Waveshare ESP32-S3 Touch LCD 2.8 2D diagram.png` (2D dimensions).
- `docs/esp32-s3-touch-lcd-2_8.stp` (3D reference for fit and clearance).
- Datasheets or measured dimensions for SPS30, SCD40 board, USB-C extension port, and the LiPo battery.

## Step-by-step plan (render/check at each step)

1. **Collect reference dimensions**
   - Measure the Waveshare 2.8" ESP-32 LCD (2D diagram + STEP).
   - Identify: outer PCB footprint, display active area, button locations (right side), USB-C location on the dev board (for the extension cable).
   - Collect SPS30 + SCD40 board dimensions and airflow inlet/outlet locations.
   - Measure the LiPo battery size and connector clearance.
   - Measure the USB-C female port and panel opening.
   - **Render/check:** make a quick OpenSCAD layout scene with bounding boxes to validate clearances.

2. **Define global parameters (OpenSCAD)**
   - Set key parameters in OpenSCAD: wall thickness, front angle, bezel margin, corner radius, standoff heights, screw boss diameter, vent slot size/pitch, battery recess depth, slide-rail clearances.
   - **Render/check:** confirm placeholder shapes update when parameters change.

3. **Model the fused main body (front display housing + rear sensor cabinet)**
   - Create the angled front enclosure with rounded corners.
   - Cut the display window opening so the Waveshare display sits flush.
   - Add three right-side button access holes aligned to the board buttons.
   - Add the display bottom vent on the main body.
   - Block out the rear sensor chamber volume and internal divider.
   - **Render/check:** verify angles, window placement, and button alignment.

4. **Design the display rear cover (board mount + battery recess)**
   - Build the rear cover that mates to the main body.
   - Add M2.5 screw bosses aligned to the display board mounting holes so the board is secured to this cover.
   - Add a recessed pocket sized for the LiPo battery and cable routing.
   - Add the top vent in the cover.
   - **Render/check:** confirm the board installs from the back and screws are accessible.

5. **Design the sensor chamber details**
   - Add mounting shelves/locators for the SPS30 and SCD40.
   - Provide clearance for the USB-C extension cable routing.
   - Add slide-in rail features for the sensor rear door.
   - **Render/check:** verify sensor fit and cable paths.

6. **Design the sensor rear cover (slide-in door)**
   - Create the slide-in door geometry with a USB-C opening.
   - Keep venting off the door for now; add vents after fit is validated.
   - **Render/check:** confirm slide fit and USB-C alignment.

7. **Add sensor chamber vents to the main body**
   - Add two bottom vents in the sensor chamber area to match the reference style.
   - **Render/check:** verify vent placement and structural strength.

8. **Assembly features and tolerances**
   - Add alignment keys, screw access clearances, and wall thickness adjustments.
   - Verify printability (overhangs, supports) for each component.
   - **Render/check:** review assembly fit with section and back views.

9. **Final validation**
   - Check overall proportions vs. the reference design.
   - Verify button access, USB-C opening, and sensor airflow paths.
   - **Render/check:** final multi-angle renders for all components.

## Deliverables
- OpenSCAD source files for each component.
- STLs per part in `cad/`.
- Rendered images in `renders/` (iso, front, right, back, top per step).

## Iteration notes
- After each step, record measurements, parameter changes, and render screenshots.
- Keep the design parametric so board or battery changes remain low effort.
