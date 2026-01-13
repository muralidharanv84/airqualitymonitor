# Step 2 - Global parameters (OpenSCAD)

## Scope
Define the audited parameter set for the enclosure so the model stays fully parametric. Values below are the tuned baseline; only items labeled tunable should be revisited after the first overlay fit check.

## Parameter table (mm unless noted)

| Parameter | Value / Formula | Notes |
| --- | --- | --- |
| `tp_w` | 50.54 | Touch panel outer width (from 2D diagram). |
| `tp_h` | 73.06 | Touch panel outer height. |
| `tp_corner_rad` | 2.0 | Corner radius on touch panel. |
| `tp_stack_thk` | 3.6 | TP + LCD stack thickness. |
| `touch_visible_w` | 43.80 | Touch visible width. |
| `touch_visible_h` | 58.20 | Touch visible height. |
| `lcd_active_w` | 43.20 | LCD active width. |
| `lcd_active_h` | 57.60 | LCD active height. |
| `pcb_w` | 49.90 | ESP32 PCB width. |
| `pcb_h` | 69.00 | ESP32 PCB height. |
| `board_top_offset` | `(tp_h - pcb_h) / 2` | Board centered behind the touch panel. |
| `board_side_offset` | `(tp_w - pcb_w) / 2` | Board centered behind the touch panel. |
| `mount_hole_spacing_x` | 41.00 | Horizontal spacing between mounting hole centers. |
| `mount_hole_spacing_y` | 60.00 | Vertical spacing between mounting hole centers. |
| `screw_d` | 2.5 | M2.5 confirmed for display dev board and enclosure. |
| `screw_clear_d` | 2.7 | Clearance hole for M2.5 screws. |
| `boss_wall` | 1.2 | Boss wall thickness around screw hole. |
| `boss_od` | `screw_d + 2 * boss_wall` | Standoff/boss outer diameter. |
| `standoff_h` | 4.0 | Based on 6.0 mm front-to-PCB-back ref and 2.0 mm face. |
| `wall_thk` | 2.0 | Default enclosure wall thickness. |
| `face_thk` | 2.0 | Front face thickness. |
| `bezel_margin` | 3.0 | Margin around TP to define the front face. |
| `front_shell_w` | `tp_w + 2 * bezel_margin` | Outer front width. |
| `front_shell_h` | `tp_h + 2 * bezel_margin` | Outer front height. |
| `front_shell_rad` | `tp_corner_rad + bezel_margin` | Outer corner radius. |
| `front_shell_d` | 18.0 | Initial front shell depth (tunable). |
| `front_tilt_deg` | 70 deg | 20 deg off vertical. |
| `outer_edge_rad` | 3.0 | Soft edge treatment radius. |
| `rear_pod_h` | 58.0 | Rear pod height (locked proportion). |
| `rear_pod_rad` | `front_shell_rad` | Rear pod corner radius. |
| `divider_thk` | 2.0 | Divider between display and sensor chambers. |
| `window_clear` | 0.40 | Clearance around display window. |
| `window_w` | `touch_visible_w + 2 * window_clear` | Display cutout width. |
| `window_h` | `touch_visible_h + 2 * window_clear` | Display cutout height. |
| `window_rad` | 1.2 | Display cutout corner radius. |
| `window_offset_y` | 2.0 | Positive moves window up. |
| `pinhole_d` | 1.2 | Top pinhole diameter. |
| `pinhole_offset_y` | 4.0 | Distance from top edge. |
| `button_count` | 3 | Number of button access holes. |
| `button_hole_d` | 2.6 | Button hole diameter (tunable). |
| `button_hole_len` | 4.0 | Side access hole length (tunable). |
| `button_top_offset_board` | 7.84 | Distance from board top to first button center. |
| `button_pitch` | 7.82 | Vertical pitch between button centers. |
| `button_edge_offset_board` | 0.0 | Distance from board edge to button center. |
| `front_vent_slot_w` | 36.0 | Front vent width (single slot). |
| `front_vent_slot_h` | 2.0 | Front vent height. |
| `front_vent_offset_y` | 6.0 | Distance from bottom edge to slot center. |
| `sensor_vent_slot_w` | 18.0 | Sensor vent slot width. |
| `sensor_vent_slot_h` | 2.0 | Sensor vent slot height. |
| `sensor_vent_slot_gap` | 2.0 | Gap between sensor vents. |
| `sensor_vent_slot_count` | 2 | Two bottom vents under SPS30. |
| `sensor_vent_offset_y` | 6.0 | Distance from bottom edge to slot center. |
| `display_lid_vent_slot_w` | 18.0 | Display cover vent width. |
| `display_lid_vent_slot_h` | 2.0 | Display cover vent height. |
| `display_lid_vent_offset_y` | 6.0 | Distance from top edge to slot center. |
| `sps30_body_w` | 41.0 | SPS30 body width. |
| `sps30_body_h` | 41.0 | SPS30 body height. |
| `sps30_body_d` | 12.0 | SPS30 body depth. |
| `sps30_mount_clear` | 0.6 | Clearance around SPS30 body. |
| `sps30_adhesive_thk` | 0.5 | Adhesive pad thickness. |
| `scd40_board_w` | 60.0 | SCD40 board width. |
| `scd40_board_h` | 17.0 | SCD40 board height. |
| `scd40_board_d` | 10.0 | SCD40 board depth. |
| `scd40_mount_clear` | 0.6 | Clearance around SCD40 board. |
| `batt_w` | 51.0 | Battery width. |
| `batt_h` | 40.0 | Battery height. |
| `batt_d` | 10.0 | Battery depth. |
| `batt_clear` | 0.6 | Clearance in battery pocket. |
| `batt_cable_clear` | 3.0 | Cable clearance at battery connector. |
| `wiring_clear` | 4.0 | Cable clearance in sensor chamber. |
| `sensor_door_thk` | 2.0 | Sensor slide-in door thickness. |
| `rear_pod_d` | `max(sps30..., scd40...)` | Set by sensor depth + wiring + door. |
| `rear_slide_clear` | 0.30 | Clearance for slide-in rails. |
| `rear_rail_thk` | 1.6 | Rail thickness for slide-in door. |
| `rear_detent_h` | 0.6 | Detent height to retain the door. |
| `rear_notch_w` | 8.0 | Pull notch width. |
| `rear_notch_h` | 3.0 | Pull notch height. |
| `usb_c_open_w` | 9.0 | USB-C opening width. |
| `usb_c_open_h` | 4.0 | USB-C opening height. |
| `usb_c_open_r` | 1.0 | USB-C opening corner radius. |
| `usb_c_open_offset_y` | 0.0 | Vertical offset from door center. |
| `rear_grille_recess_depth` | 1.0 | Depth of rear grille recess. |
| `rear_grille_margin` | 6.0 | Side margin for rear grille. |
| `rear_grille_slot_w` | `front_shell_w - 2 * rear_grille_margin` | Rear grille slot width. |
| `rear_grille_slot_h` | 2.0 | Rear grille slot height. |
| `rear_grille_slot_gap` | 1.5 | Rear grille slot gap. |
| `rear_grille_slot_count` | 7 | Number of rear grille slots. |
| `foot_d` | 6.0 | Foot diameter. |
| `foot_h` | 1.5 | Foot height. |
| `foot_inset_x` | 6.0 | Foot inset from side edge. |
| `foot_inset_y` | 6.0 | Foot inset from rear edge. |

## Notes
- SPS30 orientation: keep the green Sensirion face down (ground-facing) per the placement guide. The sensor door stays solid for now; vent slots will be added after fit is validated.
- Adhesive mounting is assumed for SPS30; model a flat mounting shelf sized to `sps30_body_*` with `sps30_adhesive_thk` allowance.
- Waveshare wiki "Dimensions" confirms **73.06 × 50.54 mm** overall; no additional offsets beyond the 2D diagram were provided.
- SCD40 board dimensions are now known; `scd40_board_*` can be treated as fixed values.

## Step 2 completion check
- Parameter block will live in the top of the OpenSCAD files (or a shared include) with the names above.
- Placeholder primitives should reference `front_shell_*`, `window_*`, and `pcb_*` so parameter updates propagate.
