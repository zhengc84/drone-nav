import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from tf_transformations import quaternion_from_euler

class OdomTfPublisher(Node):
    def __init__(self):
        super().__init__('odom_tf_publisher')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.static_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_lidar_transform()

        self.sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            qos_profile
        )
        self.tf_broadcaster = TransformBroadcaster(self)
        
    def odom_callback(self, msg):

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()  # Use current ROS time
        t.header.frame_id = 'map'                         # Assume odometry is in map frame
        t.child_frame_id = 'base_link'                      # The vehicle frame
        
        # Position from odometry
        t.transform.translation.x = float(msg.position[1])
        t.transform.translation.y = float(msg.position[0])
        t.transform.translation.z = -float(msg.position[2])
        
        # Orientation quaternion from odometry
        t.transform.rotation.x = float(msg.q[1])
        t.transform.rotation.y = float(msg.q[2])
        t.transform.rotation.z = float(msg.q[3])
        t.transform.rotation.w = float(msg.q[0])
        
        # self.get_logger().info(
        #     f"Received Odometry:\n"
        #     f"  Position: x={t.transform.translation.x:.2f}, y={t.transform.translation.y:.2f}, z={t.transform.translation.z:.2f}\n"
        #     f"  Orientation (quat): x={t.transform.rotation.x:.2f}, y={t.transform.rotation.y:.2f}, "
        #     f"z={t.transform.rotation.z:.2f}, w={t.transform.rotation.w:.2f}"
        # )

        self.tf_broadcaster.sendTransform(t)
    
    def publish_static_lidar_transform(self):
        static_tf = TransformStamped()
        static_tf.header.stamp = self.get_clock().now().to_msg()
        static_tf.header.frame_id = 'base_link'  # or 'base_link'
        static_tf.child_frame_id = 'x500_lidar_front_0/lidar_sensor_link/lidar'

        # Offset from vehicle → lidar_frame (adjust these values!)
        static_tf.transform.translation.x = 0.45
        static_tf.transform.translation.y = 0.0
        static_tf.transform.translation.z = 0.35

        q = quaternion_from_euler(1.57, 0.0, 0.0)
        static_tf.transform.rotation.x = float(q[0])
        static_tf.transform.rotation.y = float(q[1])
        static_tf.transform.rotation.z = float(q[2])
        static_tf.transform.rotation.w = float(q[3])

        self.static_broadcaster.sendTransform(static_tf)
        self.get_logger().info("Published static TF for LIDAR")

def main(args=None):
    rclpy.init(args=args)
    node = OdomTfPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
