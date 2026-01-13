// Air Quality Monitor front shell - Steps 3-4 (OpenSCAD)
// Units: mm
$fn = 64;

// Display module dimensions (from Waveshare 2D diagram)
tp_w = 50.54;
tp_h = 73.06;
tp_corner_rad = 2.0;
touch_visible_w = 43.80;
touch_visible_h = 58.20;
pcb_w = 49.90;
pcb_h = 69.00;

// Shell parameters
wall_thk = 2.0;
bezel_margin = 3.0;
front_shell_w = tp_w + 2 * bezel_margin;
front_shell_h = tp_h + 2 * bezel_margin;
front_shell_d = 18.0;        // Front shell depth (tunable)
front_shell_rad = tp_corner_rad + bezel_margin;
face_thk = 2.0;              // Front face thickness

// Window cutout
window_clear = 0.4;
window_w = touch_visible_w + 2 * window_clear;
window_h = touch_visible_h + 2 * window_clear;
window_rad = 1.2;

// Button access (from diagram) - side press
button_count = 3;
button_hole_d = 2.6;
button_top_offset_board = 7.84; // Distance from board top to first button center
button_pitch = 7.82;            // Vertical pitch between button centers
button_edge_offset_board = 0.0; // Distance from board edge to button center
button_hole_len = 4.0;          // Length of side access hole

// Front intake vent slots
front_vent_slot_w = 18.0;
front_vent_slot_h = 2.0;
front_vent_slot_gap = 1.5;
front_vent_slot_count = 3;
front_vent_offset_y = 6.0;   // Distance from bottom edge to slot center

// Display board mounting
screw_d = 2.5;               // M2.5
screw_clear_d = 2.7;
boss_wall = 1.2;
boss_od = screw_d + 2 * boss_wall;
standoff_h = 4.0;
mount_hole_spacing_x = 41.00;
mount_hole_spacing_y = 60.00;

// USB port clearance (bottom)
usb_cut_w = 10.0;
usb_cut_h = 4.0;
usb_cut_d = 12.0;

module rounded_rect(w, h, r) {
  offset(r = r) square([w - 2 * r, h - 2 * r], center = true);
}

module standoff_at(x, y) {
  translate([x, y, face_thk])
    difference() {
      cylinder(h = standoff_h, d = boss_od);
      translate([0, 0, -0.1])
        cylinder(h = standoff_h + 0.2, d = screw_clear_d);
    }
}

module front_shell() {
  inner_w = front_shell_w - 2 * wall_thk;
  inner_h = front_shell_h - 2 * wall_thk;
  inner_r = max(front_shell_rad - wall_thk, 0.6);
  board_top_offset = (tp_h - pcb_h) / 2;
  board_side_offset = (tp_w - pcb_w) / 2;
  button_top_offset_y = bezel_margin + board_top_offset + button_top_offset_board;
  button_edge_offset_x = bezel_margin + board_side_offset + button_edge_offset_board;

  difference() {
    union() {
      // Outer body
      linear_extrude(height = front_shell_d)
        rounded_rect(front_shell_w, front_shell_h, front_shell_rad);

      // Mount standoffs (board centered)
      standoff_at(mount_hole_spacing_x / 2, mount_hole_spacing_y / 2);
      standoff_at(-mount_hole_spacing_x / 2, mount_hole_spacing_y / 2);
      standoff_at(mount_hole_spacing_x / 2, -mount_hole_spacing_y / 2);
      standoff_at(-mount_hole_spacing_x / 2, -mount_hole_spacing_y / 2);
    }

    // Inner cavity (open back)
    translate([0, 0, face_thk])
      linear_extrude(height = front_shell_d - face_thk)
        rounded_rect(inner_w, inner_h, inner_r);

    // Display window opening
    translate([0, 0, -0.1])
      linear_extrude(height = face_thk + 0.2)
        rounded_rect(window_w, window_h, window_rad);

    // Side button access holes (right side)
    for (i = [0 : button_count - 1]) {
      y_pos = front_shell_h / 2 - button_top_offset_y - i * button_pitch;
      x_pos = front_shell_w / 2 - wall_thk / 2;
      translate([x_pos, y_pos, front_shell_d / 2])
        rotate([0, 90, 0])
          cylinder(h = button_hole_len, d = button_hole_d, center = true);
    }

    // Front intake vent slots
    slot_total_w = front_vent_slot_count * front_vent_slot_w
                   + (front_vent_slot_count - 1) * front_vent_slot_gap;
    slot_start_x = -slot_total_w / 2 + front_vent_slot_w / 2;
    for (i = [0 : front_vent_slot_count - 1]) {
      x_pos = slot_start_x + i * (front_vent_slot_w + front_vent_slot_gap);
      y_pos = -front_shell_h / 2 + front_vent_offset_y;
      translate([x_pos, y_pos, -0.1])
        cube([front_vent_slot_w, front_vent_slot_h, face_thk + 0.2], center = true);
    }

    // USB port opening on bottom edge
    translate([0, -front_shell_h / 2 + wall_thk / 2, usb_cut_d / 2])
      cube([usb_cut_w, wall_thk + 0.4, usb_cut_d], center = true);
  }
}

front_shell();
