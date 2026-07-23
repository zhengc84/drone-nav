import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import MarkerArray
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class TrajectoryToPose(Node):
    def __init__(self):
        super().__init__('trajectory_to_pose_node')
        sub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.subscription = self.create_subscription(
            MarkerArray,
            '/trajectory_node_list',
            self.marker_callback,
            sub_qos
        )

        self.pose_pub = self.create_publisher(PoseStamped, '/cartographer/pose', pub_qos)

    def marker_callback(self, msg):
        latest_point = None

        # Iterate through markers to find the last point in any LINE_STRIP
        for marker in msg.markers:
            if marker.type == 4 and marker.points:  # LINE_STRIP == 4
                latest_point = marker.points[-1]

        if latest_point:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = 'map'

            self.get_logger().info(
                f"  latest point: {latest_point}"
            )
            pose_msg.pose.position = latest_point
            pose_msg.pose.orientation.w = 1.0  # Neutral orientation

            self.pose_pub.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryToPose()
    rclpy.spin(node)
    rclpy.shutdown()
