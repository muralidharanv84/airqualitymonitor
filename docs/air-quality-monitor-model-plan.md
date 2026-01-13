# Air Quality Monitor 3D Model Plan (Qingping Air Quality Monitor 2 reference)

## Goal
Create a parametric, printable 3D enclosure inspired by the Qingping Air Quality Monitor 2. The model must closely match the reference image proportions and key features while fitting the listed components.

The enclosure is a 3-part assembly:
- Main body: angled front display housing fused with the rear sensor cabinet.
- Display rear cover: mounts the display PCB and holds the battery.
- Sensor rear cover: slide-in door with USB-C opening (vents added later).

## Visual reference breakdown (from image)
- Front face: rectangular with large corner radii, slightly thicker frame around the screen.
- Screen: sits behind a bezel with a thin, even reveal; black mask has rounded corners.
- Front vent: a single thin horizontal slot centered beneath the display window.
- Small pinhole above the screen (likely mic/sensor) centered on the top of the face.
- Right-side: 3 discrete button access holes aligned vertically.
- Body profile: front face leans back (angled), with a softly rounded transition into the rear pod.
- Rear sensor pod: rounded rectangular box, same width as the front face, shorter height, deeper than the front face.
- Rear grille: multiple horizontal slats across most of the rear face.
- Central recess on rear grille: rounded-rectangle inset with a USB-C opening centered.
- Underside: 4 round feet, slightly inset from the corners.

This is the crude ascii art version of the expected side profile of the air quality monitor when it's complete
                   ___
                  /  /
                 /  /
                /  /
               /  /
              /  /
             /  ------------|
            /               |
           / _______________|

Note: Colors and surface finish in the reference are matte with soft shadows; the model should prioritize geometry and proportions.

## Critical dimensions (from assets and notes)
Source: `docs/Waveshare ESP32-S3 Touch LCD 2.8 2D diagram.png`

Display / Touch panel:
- Touch panel overall: 50.54 mm (W) x 73.06 mm (H)
- Touch visible area: 43.80 mm (W) x 58.20 mm (H)
- LCD active area: 43.20 mm (W) x 57.60 mm (H)
- Touch panel corner radius: R2.0 mm
- TP + LCD stack thickness: 3.6 mm
- Overall depth shown: 10.0 mm (reference stack depth)

Display PCB:
- PCB overall: 49.90 mm (W) x 69.00 mm (H)
- Mount hole spacing: 41.00 mm (X) x 60.00 mm (Y)
- Button offsets: use diagram values for top offset and pitch

Sensors and battery (from notes):
- SPS30: 41.0 mm x 41.0 mm x 12.0 mm (body)
- SCD40 board: 60.0 mm x 17.0 mm x 10.0 mm
- LiPo battery: 51 mm x 40 mm x 10 mm, connector on top

Ports:
- USB-C opening (extension port): nominal 9.0 mm (W) x 4.0 mm (H), adjust after measuring port bezel

## Target proportions (derived from display + reference image)
These define the overall feel. Confirm by render overlay against the reference image.

- Front face outer size: tp_w + 2 * bezel_margin (use 3.0 mm margin to start)
  - Expected: ~56.5 mm (W) x ~79.1 mm (H)
- Outer corner radius: tp_corner_rad + bezel_margin (start at ~5.0 mm)
- Front face thickness: 2.0 mm
- Front tilt: 70 deg (20 deg off vertical)
- Front shell depth (angled portion): 16 to 20 mm initial
- Rear sensor pod depth: set by fit (as large as necessary to clear SPS30/SCD40 + wiring + door)
- Rear pod height: ~55 to 60 mm (visually shorter than front face)
- Fillet/chamfer: soft radius on all external edges, 2.5 to 4.0 mm

## Overlay render + proportion lock
- Overlay render: `renders/air-quality-monitor-overlay-front.png`
- Locked outer proportions (based on overlay + display dimensions):
  - Front face: 56.54 mm (W) x 79.06 mm (H)
  - Corner radius: 5.0 mm
  - Window offset: +2.0 mm up from center (to open space for the vent below)
  - Rear pod height: 58.0 mm (approx 0.73 of front face height)

## Functional layout and clearances
- Display board installs from the rear into the main body and is secured to the display rear cover via M2.5 screws.
- Display rear cover includes a recessed battery pocket and a cable channel to the board.
- SPS30 mounts on a shelf with adhesive; keep inlet/outlet aligned to bottom vents.
- SCD40 board mounts to a side wall (tape or small tabs); keep gas inlet unobstructed.
- Sensor rear cover slides in with rails and a detent; no screws.
- Main body includes:
  - One front vent slot under the display.
  - Two bottom vents under the sensor chamber.
- Display rear cover includes:
  - One top vent slot.
- Sensor rear cover includes:
  - USB-C opening and pull notch. Vent slots are added after fit is validated.

## Modeling approach (OpenSCAD)
- Use modular files: main body, display rear cover, sensor rear cover.
- Keep all critical dimensions parameterized in a shared include (`cad/air-quality-monitor-params.scad`).
- Use a layout scene (`cad/air-quality-monitor-layout.scad`) to visualize component blocks and verify alignment before cutting details.

## Detailed plan (from scratch)

1. Collect and confirm dimensions (done)
   - [x] Extract all dimensions from the display 2D diagram.
   - [x] SCD40 board size set to 60.0 x 17.0 x 10.0 mm.
   - [x] Battery size set to 51 x 40 x 10 mm.
   - [x] USB-C opening set to 9.0 x 4.0 mm (confirm bezel depth later).
   - [x] Record measurements in `cad/air-quality-monitor-params.scad`.
   - [x] Layout scene created in `cad/air-quality-monitor-layout.scad`.

2. Establish global parameters (done)
   - [x] Define wall thickness, corner radius, bezel margin, front tilt, and depth logic.
   - [x] Define clearances for PCB, sensors, battery, and slide rails.
   - [x] Parameter audit completed in `cad/air-quality-monitor-params.scad`.

3. Build the front display housing (main body, part 1)
   - Create the front face as a rounded-rectangle shell with the specified tilt.
   - Cut the display window to the touch visible area with clearance.
   - Add a thin bezel lip if needed to mimic the reference screen framing.
   - Add the front vent slot centered below the display (long, thin).
   - Add the small pinhole above the screen.
   - Render/check: front and 3/4 view vs. reference image.

4. Add the right-side button access holes
   - Use diagram offsets and pitch to align to the board.
   - Create three side holes sized for tactile access (2.6 to 3.0 mm dia, 4.0 mm length).
   - Render/check: side view shows alignment with the PCB buttons.

5. Build the rear sensor pod (main body, part 2)
   - Create the rear pod as a rounded-rectangle volume fused to the back of the front housing.
   - Ensure width matches the front face; set height shorter than the front face to match the reference.
   - Add the inner divider between display chamber and sensor chamber.
   - Render/check: overall silhouette matches the reference when viewed from side and rear.

6. Add interior mounting features in main body
   - Add shelves for SPS30 and SCD40 (adhesive pads or tabs).
   - Provide cable routing channel from sensor chamber to display area.
   - Add slide rail pockets for the sensor rear cover.
   - Render/check: section view to confirm clearances.

7. Design the display rear cover
   - Create a cover that mates to the front housing with a clean seam.
   - Add M2.5 standoffs aligned to the PCB mount holes (41.00 x 60.00 mm spacing).
   - Add a recessed battery pocket sized to 51 x 40 x 10 mm with clearance.
   - Add a top vent slot (single, thin, centered).
   - Render/check: board and battery placement works in the layout scene.

8. Design the sensor rear cover (slide-in door)
   - Create a slide-in panel with matching outer radius and thickness.
   - Add a USB-C opening centered in a recessed pill-shaped area.
   - Add a small pull notch to remove the door.
   - Render/check: sliding fit and USB-C alignment.

9. Add sensor chamber vents to main body
   - Create two bottom vent slots under the SPS30 area.
   - Align vents with SPS30 inlet/outlet orientation (use placement guide).
   - Render/check: underside view shows vents and foot spacing.

10. Add underside feet and soft edge treatment
   - Add 4 round feet, slightly inset from the corners (reference shows 4 round pads).
   - Add outer fillets or chamfers to soften edges (2.5 to 4.0 mm radius).
   - Render/check: underside and 3/4 views match the reference stance.

11. Assembly validation
   - Verify: display fits from the rear, screw access works, battery is recessed, sensor components fit with clearance, slide door is removable.
   - Check for printability: avoid impossible overhangs, ensure vent slots are printable.
   - Render/check: full assembly from iso, front, right, back, top, bottom.

12. Final proportion check and iteration
   - Compare renders to the reference image for tilt angle, pod height, vent slot position, and corner radii.
   - Adjust parameters and re-render until the silhouette matches.

## Deliverables
- OpenSCAD sources: main body, display rear cover, sensor rear cover.
- STL exports for each part in `cad/`.
- Renders in `renders/` (iso, front, right, back, top, bottom).

## Validation checklist
- Display window aligned to LCD active area with clearance.
- Button holes align with the PCB buttons.
- Front vent slot centered under screen.
- Rear pod height and depth match reference proportions.
- SPS30 and SCD40 fit with clearance and airflow path.
- USB-C opening aligns with extension port.
- Battery pocket fits with cable routing.
- Slide door fits smoothly with detent.
