# Step 1 - Reference dimensions + prep notes

## Plan review (quick sanity)
- The plan is well-structured: parameter-driven modeling, separate components, and render checkpoints per step are appropriate for a print-ready enclosure.
- Step order makes sense (collect dimensions first, then parameters, then shells and internals).
- I can proceed with Step 1 by extracting the LCD board dimensions from the provided 2D diagram and flagging the remaining measurements needed for the SPS30 placement details and the USB-C extension port.

## Measurements extracted from provided assets
Source: `docs/Waveshare ESP32-S3 Touch LCD 2.8 2D diagram.png`

### Front face / display window
- Overall front width (TP DD): **50.54 ± 0.05 mm**
- Overall front height (TP DD): **73.06 ± 0.05 mm**
- Touch panel visible area (TP VA): **43.80 ± 0.15 mm** (W) × **58.20 ± 0.15 mm** (H)
- LCD active area (LCD AA): **43.20 mm** (W) × **57.60 mm** (H)
- Corner radius: **R2.00 mm** (4x)

### Side view / thickness cues
- TP + LCD stack thickness: **3.60 mm**
- Lens thickness: **0.70 mm**
- Overall depth shown: **10.00 mm**
- Internal reference depth shown: **6.00 mm**

### Rear PCB / mounting layout
- Overall PCB width: **49.90 mm**
- Overall PCB height: **69.00 mm**
- Inner width reference: **41.00 mm**
- Inner height reference: **60.00 mm**
- Top/border reference: **4.50 mm**
- Right-side reference: **1.9 mm**
- Left-side button stack references (top to bottom): **7.84 mm**, **7.82 mm**, **7.86 mm**, **10.86 mm** (as shown)
- Bottom connector spacing references: **9.00 mm**, **11.6 mm**, **11.4 mm** (as shown)

### SPS30 sensor module (internet reference)
- Overall body size: **~41 mm × 41 mm × 12 mm** (SparkFun SPS30 product page notes “just under 41mm x 41mm x 12mm”). Source: https://www.sparkfun.com/particulate-matter-sensor-sps30.html

### SCD40 board (provided)
- Overall board size: **60 mm x 17 mm x 10 mm**.

## Assembly + placement notes (from latest input)
- SCD40 board can be taped or glued to the sensor enclosure side wall.
- Battery size: **51 mm × 40 mm × 10 mm**, connector on top.
- Use the same screw size as the display dev board for standoffs and enclosure assembly.
- Prefer a slide-in/slide-out rear wall for the sensor enclosure (no screws) to improve serviceability.
- USB-C extension port needs a panel opening on the rear slide-in door.

## User answers and decisions
- SPS30 placement guide reference: use the attached Sensirion placement guide image; keep the rear slide-in wall solid for now (no vent slots) and add venting to that lid as the final step.
- SPS30 mounting: adhesive mounting (no screw holes on the module).
- Slide-in rear wall approach: I will proceed with a keyed rail + detent approach that slides in from the rear, with a small pull notch for removal.

## Step 1 remaining data to collect
- SPS30 inlet/outlet positions and keepout zones (placement guide confirms orientation, but detailed offsets are still needed for precise vent alignment later).
- USB-C extension female port dimensions (opening size + bezel depth).
- Preferred PCB standoff height once screw size is confirmed on the display dev board.
