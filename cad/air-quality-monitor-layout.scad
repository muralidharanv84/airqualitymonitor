// Air Quality Monitor layout scene (bounding boxes + front overlay)
include <air-quality-monitor-params.scad>;

show_front_overlay = true;
show_layout_boxes = true;

module rounded_rect_2d(w, h, r) {
  offset(r = r) square([w - 2 * r, h - 2 * r], center = true);
}

module front_overlay_2d() {
  // Front face outline
  linear_extrude(height = 1)
    rounded_rect_2d(front_shell_w, front_shell_h, front_shell_rad);

  // Display window outline
  translate([0, window_offset_y, 0])
    linear_extrude(height = 1)
      rounded_rect_2d(window_w, window_h, window_rad);

  // Front vent slot (single)
  translate([0, -front_shell_h / 2 + front_vent_offset_y, 0])
    linear_extrude(height = 1)
      square([front_vent_slot_w, front_vent_slot_h], center = true);

  // Pinhole
  translate([0, front_shell_h / 2 - pinhole_offset_y, 0])
    linear_extrude(height = 1)
      circle(d = pinhole_d);
}

module layout_boxes() {
  // Front housing volume (approx)
  color([0.8, 0.8, 0.8, 0.4])
    translate([0, 0, front_shell_d / 2])
      cube([front_shell_w, front_shell_h, front_shell_d], center = true);

  // Rear pod volume (approx)
  color([0.7, 0.7, 0.7, 0.4])
    translate([0, -((front_shell_h - rear_pod_h) / 2), front_shell_d + rear_pod_d / 2])
      cube([front_shell_w, rear_pod_h, rear_pod_d], center = true);

  // Display PCB bounding box
  color([0.2, 0.6, 0.9, 0.5])
    translate([0, 0, face_thk + tp_stack_thk / 2])
      cube([pcb_w, pcb_h, tp_stack_thk], center = true);

  // SPS30 bounding box
  color([0.9, 0.6, 0.2, 0.6])
    translate([0, -((front_shell_h - rear_pod_h) / 2), front_shell_d + rear_pod_d / 2])
      cube([sps30_body_w, sps30_body_h, sps30_body_d], center = true);

  // SCD40 bounding box
  color([0.3, 0.8, 0.4, 0.6])
    translate([0, -((front_shell_h - rear_pod_h) / 2) + 10, front_shell_d + rear_pod_d / 2])
      cube([scd40_board_w, scd40_board_h, scd40_board_d], center = true);

  // Battery bounding box (display cover)
  color([0.7, 0.4, 0.8, 0.5])
    translate([0, 0, face_thk + tp_stack_thk + batt_d / 2 + 2])
      cube([batt_w, batt_h, batt_d], center = true);
}

if (show_front_overlay) {
  front_overlay_2d();
}

if (show_layout_boxes) {
  layout_boxes();
}
