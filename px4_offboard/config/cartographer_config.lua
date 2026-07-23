include "map_builder.lua"
include "trajectory_builder.lua"


POSE_GRAPH.optimization_problem.huber_scale = 1e1
POSE_GRAPH.optimization_problem.acceleration_weight = 500.0
POSE_GRAPH.optimization_problem.rotation_weight = 500.0

POSE_GRAPH.optimize_every_n_nodes = 30
POSE_GRAPH.constraint_builder.sampling_ratio = 0.0

MAP_BUILDER.use_trajectory_builder_3d = true
TRAJECTORY_BUILDER_3D.num_accumulated_range_data = 5
TRAJECTORY_BUILDER_3D.imu_gravity_time_constant = 0.1
TRAJECTORY_BUILDER_3D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_3D.min_range = 0.1
TRAJECTORY_BUILDER_3D.motion_filter.max_time_seconds = 0.5
TRAJECTORY_BUILDER_3D.motion_filter.max_distance_meters = 0.1
TRAJECTORY_BUILDER_3D.motion_filter.max_angle_radians = math.rad(1.0)
TRAJECTORY_BUILDER_3D.max_range = 30.0
TRAJECTORY_BUILDER_3D.voxel_filter_size = 0.1
TRAJECTORY_BUILDER_3D.high_resolution_adaptive_voxel_filter.max_length = 1.0
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.translation_weight = 1.0
TRAJECTORY_BUILDER_3D.ceres_scan_matcher.rotation_weight = 10.0
TRAJECTORY_BUILDER_3D.use_online_correlative_scan_matching = false

-- trust imu slam more
POSE_GRAPH.optimization_problem.local_slam_pose_translation_weight = 1e4
POSE_GRAPH.optimization_problem.local_slam_pose_rotation_weight = 1e4
options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_link",
  published_frame = "base_link",
  odom_frame = "odom",
  provide_odom_frame = true,
  use_odometry = false,
  use_nav_sat = false,
  use_landmarks = false,
  publish_frame_projected_to_2d = false,
  use_pose_extrapolator = true,
  num_laser_scans = 0,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 1,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 0.005,
  trajectory_publish_period_sec = 0.03,
  rangefinder_sampling_ratio = 1.0,
  odometry_sampling_ratio = 1.0,
  fixed_frame_pose_sampling_ratio = 1.0,
  imu_sampling_ratio = 1.0,
  landmarks_sampling_ratio = 1.0
}




return options
