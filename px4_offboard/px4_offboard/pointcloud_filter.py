import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class PointCloudFilter(Node):
    def __init__(self):
        super().__init__('pointcloud_filter')
        self.sub = self.create_subscription(
            PointCloud2,
            '/lidar/data/points',
            self.pc_callback,
            10)
        self.pub = self.create_publisher(PointCloud2, '/lidar/data/points_filtered', 10)

    def pc_callback(self, msg):
        # Read points, skipping NaNs and invalids
        raw_points = list(pc2.read_points(msg, skip_nans=True))
        if not raw_points:
            self.get_logger().warn('No valid points after filtering!')
            return
        
        points = [(p[0], p[1], p[2]) for p in raw_points]
        # Create a new PointCloud2 message from filtered points
        filtered_pc = pc2.create_cloud_xyz32(msg.header, points)
        filtered_pc.header.stamp = self.get_clock().now().to_msg()

        filtered_pc.is_dense = True  # Mark as dense now
        self.pub.publish(filtered_pc)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
