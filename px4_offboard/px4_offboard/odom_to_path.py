import rclpy
from rclpy.node import Node

from px4_msgs.msg import VehicleOdometry
from geometry_msgs.msg import PoseStamped
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from builtin_interfaces.msg import Time

class OdometryConverter(Node):
    def __init__(self):
        super().__init__('odometry_to_pose_converter')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            qos_profile
        )

        self.pub = self.create_publisher(
            PoseStamped,
            '/vehicle_pose',
            pub_qos
        )

    def odom_callback(self, msg: VehicleOdometry):
        pose_msg = PoseStamped()

        # Convert timestamp from microseconds to ROS time
        sec = msg.timestamp // 1_000_000
        nanosec = (msg.timestamp % 1_000_000) * 1000
        pose_msg.header.stamp = Time(sec=sec, nanosec=nanosec)

        # Frame ID (set as needed)
        pose_msg.header.frame_id = "map"

        # Position: NED to ENU conversion (optional)
        pose_msg.pose.position.x = float(msg.position[1])  # North → Y
        pose_msg.pose.position.y = float(msg.position[0])  # East → X
        pose_msg.pose.position.z = float(-msg.position[2]) # Down → Up

        # Orientation: same quaternion, but must rotate if NED → ENU
        pose_msg.pose.orientation.x = float(msg.q[0])
        pose_msg.pose.orientation.y = float(msg.q[1])
        pose_msg.pose.orientation.z = float(msg.q[2])
        pose_msg.pose.orientation.w = float(msg.q[3])

        self.pub.publish(pose_msg)

def main():
    rclpy.init()
    node = OdometryConverter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
