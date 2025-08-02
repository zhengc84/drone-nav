import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from rclpy.time import Time
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy


class PointCloudTimestampFixer(Node):
    def __init__(self):
        super().__init__('pc_timestamp_fixer')

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
        self.sub = self.create_subscription(
            PointCloud2,
            '/lidar/data/points',
            self.callback,
            sub_qos)
        self.pub = self.create_publisher(PointCloud2, '/lidar/fixed_points', pub_qos)

    def callback(self, msg):
        msg.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudTimestampFixer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
