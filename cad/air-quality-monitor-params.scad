// Air Quality Monitor shared parameters (mm)
$fn = 64;

// Display module dimensions (Waveshare 2.8" ESP32-S3)
tp_w = 50.54;
tp_h = 73.06;
tp_corner_rad = 2.0;
tp_stack_thk = 3.6;
touch_visible_w = 43.80;
touch_visible_h = 58.20;
lcd_active_w = 43.20;
lcd_active_h = 57.60;

// Display PCB
pcb_w = 49.90;
pcb_h = 69.00;
board_top_offset = (tp_h - pcb_h) / 2;
board_side_offset = (tp_w - pcb_w) / 2;
mount_hole_spacing_x = 41.00;
mount_hole_spacing_y = 60.00;

// Fasteners
screw_d = 2.5;          // M2.5
screw_clear_d = 2.7;
boss_wall = 1.2;
boss_od = screw_d + 2 * boss_wall;
standoff_h = 4.0;

// Enclosure shell
wall_thk = 2.0;
face_thk = 2.0;
bezel_margin = 3.0;
front_shell_w = tp_w + 2 * bezel_margin;
front_shell_h = tp_h + 2 * bezel_margin;
front_shell_rad = tp_corner_rad + bezel_margin;
front_shell_d = 18.0;
front_tilt_deg = 70;    // 20 deg off vertical
outer_edge_rad = 3.0;
rear_pod_h = 58.0;
rear_pod_rad = front_shell_rad;
divider_thk = 2.0;

// Display window
window_clear = 0.4;
window_w = touch_visible_w + 2 * window_clear;
window_h = touch_visible_h + 2 * window_clear;
window_rad = 1.2;
window_offset_y = 2.0;  // positive moves window up

// Face details
pinhole_d = 1.2;
pinhole_offset_y = 4.0; // distance from top edge

// Right-side buttons
button_count = 3;
button_hole_d = 2.6;
button_hole_len = 4.0;
button_top_offset_board = 7.84;
button_pitch = 7.82;
button_edge_offset_board = 0.0;

// Front vent (single slot)
front_vent_slot_w = 36.0;
front_vent_slot_h = 2.0;
front_vent_offset_y = 6.0; // distance from bottom edge to slot center

// Sensor vents (main body bottom)
sensor_vent_slot_w = 18.0;
sensor_vent_slot_h = 2.0;
sensor_vent_slot_gap = 2.0;
sensor_vent_slot_count = 2;
sensor_vent_offset_y = 6.0;

// Display rear cover vent (single slot)
display_lid_vent_slot_w = 18.0;
display_lid_vent_slot_h = 2.0;
display_lid_vent_offset_y = 6.0;

// Sensors
sps30_body_w = 41.0;
sps30_body_h = 41.0;
sps30_body_d = 12.0;
sps30_mount_clear = 0.6;
sps30_adhesive_thk = 0.5;

scd40_board_w = 60.0;
scd40_board_h = 17.0;
scd40_board_d = 10.0;
scd40_mount_clear = 0.6;

// Battery
batt_w = 51.0;
batt_h = 40.0;
batt_d = 10.0;
batt_clear = 0.6;
batt_cable_clear = 3.0;

// Rear pod depth (fit sensors + wiring)
wiring_clear = 4.0;
sensor_door_thk = 2.0;
rear_pod_d = max(
  sps30_body_d + sps30_mount_clear + wiring_clear + sensor_door_thk + 2.0,
  scd40_board_d + scd40_mount_clear + wiring_clear + sensor_door_thk + 2.0
);

// Sensor rear cover (slide-in)
rear_slide_clear = 0.30;
rear_rail_thk = 1.6;
rear_detent_h = 0.6;
rear_notch_w = 8.0;
rear_notch_h = 3.0;

// USB-C extension opening
usb_c_open_w = 9.0;
usb_c_open_h = 4.0;
usb_c_open_r = 1.0;
usb_c_open_offset_y = 0.0;

// Rear grille (sensor door)
rear_grille_recess_depth = 1.0;
rear_grille_margin = 6.0;
rear_grille_slot_w = front_shell_w - 2 * rear_grille_margin;
rear_grille_slot_h = 2.0;
rear_grille_slot_gap = 1.5;
rear_grille_slot_count = 7;

// Feet
foot_d = 6.0;
foot_h = 1.5;
foot_inset_x = 6.0;
foot_inset_y = 6.0;
