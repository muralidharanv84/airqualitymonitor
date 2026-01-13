// Air Quality Monitor rear shell - Step 5 (OpenSCAD)
// Units: mm
$fn = 64;

// Shared outer dimensions
// Display module dimensions (from Waveshare 2D diagram)
tp_w = 50.54;
tp_h = 73.06;
tp_corner_rad = 2.0;

// Shell parameters
wall_thk = 2.0;
bezel_margin = 3.0;
front_shell_w = tp_w + 2 * bezel_margin;
front_shell_h = tp_h + 2 * bezel_margin;
rear_shell_d = 26.0;        // Rear shell depth (tunable)
rear_shell_rad = tp_corner_rad + bezel_margin;

// Sensor chamber partition
front_chamber_d = 12.0;     // Depth from front opening to divider front face
divider_thk = 2.0;

define_inner_w = front_shell_w - 2 * wall_thk;

define_inner_h = front_shell_h - 2 * wall_thk;

define_inner_r = max(rear_shell_rad - wall_thk, 0.6);

module rounded_rect(w, h, r) {
  offset(r = r) square([w - 2 * r, h - 2 * r], center = true);
}

module rear_shell() {
  inner_w = define_inner_w;
  inner_h = define_inner_h;
  inner_r = define_inner_r;
  divider_center_z = front_chamber_d + divider_thk / 2;

  union() {
    difference() {
      // Outer body (open front/back)
      linear_extrude(height = rear_shell_d)
        rounded_rect(front_shell_w, front_shell_h, rear_shell_rad);

      // Inner cavity
      translate([0, 0, -0.1])
        linear_extrude(height = rear_shell_d + 0.2)
          rounded_rect(inner_w, inner_h, inner_r);
    }

    // Divider wall to isolate chambers (front/back)
    translate([0, 0, divider_center_z])
      cube([inner_w, inner_h, divider_thk], center = true);
  }
}

rear_shell();
