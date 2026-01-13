# Step 1 - Reference dimensions + prep notes

## Plan review (quick sanity)
- The plan is well-structured: parameter-driven modeling, separate components, and render checkpoints per step are appropriate for a print-ready enclosure.
- Step order makes sense (collect dimensions first, then parameters, then shells and internals).
- I can proceed with Step 1 by extracting the LCD board dimensions from the provided 2D diagram and flagging the remaining measurements needed for SPS30/SPS40 and the battery.

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

### SPS40 dev board (provided)
- Overall board size: **55 mm × 17 mm × 10 mm** (height includes top of sensor).

## Step 1 in progress: remaining data to collect
- SPS30 inlet/outlet positions, mounting hole spacing, and any keepout zones (ideally from the mechanical design guide).
- SPS30 mounting strategy confirmation (screws vs. posts vs. adhesive pads).
- Preferred PCB standoff height for the ESP32 board (screw size will match the display dev board).

## Assembly + placement notes (from latest input)
- SPS40 dev board can be taped or glued to the sensor enclosure side wall.
- Battery size: **51 mm × 40 mm × 10 mm**, connector on top.
- Use the same screw size as the display dev board for standoffs and enclosure assembly.
- Prefer a slide-in/slide-out rear wall for the sensor enclosure (no screws) to improve serviceability.

## Questions
1. Do you have the SPS30 mechanical design guide (or measurements) for inlet/outlet locations and mounting hole spacing?
2. Should we prioritize adhesive mounting for SPS30 as well, or keep it screw/post-mounted?
3. Any preference on the slide-in rear wall approach (e.g., friction fit, tabs + detents, or a keyed track)?
