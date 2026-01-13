# Step 2 - Global parameters (Fusion 360)

## Scope
Define the initial parameter set for the enclosure so the model stays fully parametric. Values below are the starting point; any TBD values should be confirmed before cutting hard geometry.

## Parameter table (mm unless noted)

| Parameter | Value / Formula | Notes |
| --- | --- | --- |
| `tp_w` | 50.54 | Touch panel outer width (from 2D diagram). |
| `tp_h` | 73.06 | Touch panel outer height. |
| `tp_corner_rad` | 2.0 | Corner radius on touch panel. |
| `tp_stack_thk` | 3.6 | TP + LCD stack thickness. |
| `lcd_active_w` | 43.20 | LCD active width. |
| `lcd_active_h` | 57.60 | LCD active height. |
| `touch_visible_w` | 43.80 | Touch visible width. |
| `touch_visible_h` | 58.20 | Touch visible height. |
| `pcb_w` | 49.90 | ESP32 PCB width. |
| `pcb_h` | 69.00 | ESP32 PCB height. |
| `pcb_clear` | 0.30 | Clearance around PCB in the shell. |
| `board_top_offset` | `(tp_h - pcb_h) / 2` | Board centered behind the touch panel. |
| `board_side_offset` | `(tp_w - pcb_w) / 2` | Board centered behind the touch panel. |
| `wall_thk` | 2.0 | Default enclosure wall thickness. |
| `bezel_margin` | 3.0 | Margin around TP to define the front face. |
| `front_shell_w` | `tp_w + 2 * bezel_margin` | Outer front width. |
| `front_shell_h` | `tp_h + 2 * bezel_margin` | Outer front height. |
| `front_shell_rad` | `tp_corner_rad + bezel_margin` | Outer corner radius. |
| `front_shell_d` | 18.0 | Initial front shell depth (tunable). |
| `face_thk` | 2.0 | Front face thickness. |
| `window_clear` | 0.40 | Clearance around display window. |
| `window_w` | `touch_visible_w + 2 * window_clear` | Display cutout width. |
| `window_h` | `touch_visible_h + 2 * window_clear` | Display cutout height. |
| `button_count` | 3 | Number of button holes on the right side. |
| `button_hole_d` | 2.6 | Button hole diameter (tunable). |
| `button_hole_len` | 4.0 | Length of side access hole (tunable). |
| `button_top_offset_board` | 7.84 | Distance from board top to first button center (from diagram). |
| `button_pitch` | 7.82 | Vertical pitch between button centers (from diagram). |
| `button_edge_offset_board` | 0.0 | Distance from board edge to button center. |
| `button_top_offset_y` | `bezel_margin + board_top_offset + button_top_offset_board` | Distance from front-shell top to first button center. |
| `button_edge_offset_x` | `bezel_margin + board_side_offset + button_edge_offset_board` | Distance from front-shell right edge to button center. |
| `front_tilt_deg` | 8 deg | Initial tilt; adjust after first visual check. |
| `screw_d` | 2.5 | M2.5 confirmed for display dev board and enclosure. |
| `boss_wall` | 1.2 | Boss wall thickness around screw hole. |
| `boss_od` | `screw_d + 2 * boss_wall` | Standoff/boss outer diameter. |
| `screw_clear_d` | 2.7 | Clearance hole for M2.5 screws. |
| `standoff_h` | 4.0 | Based on 6.0 mm front-to-PCB-back reference and 2.0 mm face. |
| `mount_hole_spacing_x` | 41.00 | Horizontal spacing between mounting hole centers. |
| `mount_hole_spacing_y` | 60.00 | Vertical spacing between mounting hole centers. |
| `sps30_body_w` | 41.0 | SPS30 body width. |
| `sps30_body_h` | 41.0 | SPS30 body height. |
| `sps30_body_d` | 12.0 | SPS30 body depth. |
| `sps30_adhesive_thk` | 0.5 | Foam tape or adhesive pad thickness. |
| `sps30_mount_clear` | 0.6 | Clearance around SPS30 body. |
| `sps40_board_w` | 55.0 | SPS40 dev board width. |
| `sps40_board_h` | 17.0 | SPS40 dev board height. |
| `sps40_board_d` | 10.0 | SPS40 dev board depth. |
| `sps40_mount_clear` | 0.6 | Clearance around SPS40 board. |
| `batt_w` | 51.0 | Battery width. |
| `batt_h` | 40.0 | Battery height. |
| `batt_d` | 10.0 | Battery depth. |
| `batt_clear` | 0.6 | Clearance in battery tray. |
| `front_vent_slot_w` | 18.0 | Initial front intake slot width (tunable). |
| `front_vent_slot_h` | 2.0 | Initial front intake slot height (tunable). |
| `front_vent_slot_gap` | 1.5 | Gap between intake slots (tunable). |
| `front_vent_slot_count` | 3 | Number of intake slots (tunable). |
| `rear_slide_clear` | 0.30 | Clearance for slide-in rear wall in rails. |
| `rear_rail_thk` | 1.6 | Rail thickness for the slide-in rear wall. |
| `rear_detent_h` | 0.6 | Detent height to retain the slide-in wall. |
| `rear_notch_w` | 8.0 | Pull notch width for removal. |
| `rear_notch_h` | 3.0 | Pull notch height for removal. |

## Notes
- SPS30 orientation: keep the green Sensirion face down (ground-facing) per the placement guide. Rear slide-in wall stays solid for now; vent slots will be added as the final step.
- Adhesive mounting is assumed for SPS30; model a flat mounting shelf sized to `sps30_body_*` with `sps30_adhesive_thk` allowance.
- Waveshare wiki "Dimensions" confirms **73.06 × 50.54 mm** overall; no additional offsets beyond the 2D diagram were provided.

## Step 2 completion check
- Parameter table added to Fusion 360 with the names above.
- Placeholder sketches reference `front_shell_*`, `window_*`, and `pcb_*` dimensions to confirm updates flow through the timeline.
