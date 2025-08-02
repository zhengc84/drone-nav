import rclpy
from rclpy.node import Node
from px4_msgs.msg import SensorCombined
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
import numpy as np

class SensorCombinedToImu(Node):
    def __init__(self):

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
        super().__init__('sensor_combined_to_imu')
        self.get_logger().info("started IMU pipeline")
        self.sub = self.create_subscription(
            SensorCombined,
            '/fmu/out/sensor_combined',
            self.sensor_combined_callback,
            sub_qos)
        
        self.pub = self.create_publisher(Imu, '/imu_cleaned', pub_qos)

    def sensor_combined_callback(self, msg: SensorCombined):
        imu_msg = Imu()

        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = "base_link"  # copy timestamp and frame_id if valid

        # Angular velocity from gyro
        imu_msg.angular_velocity.x = float(msg.gyro_rad[0])
        imu_msg.angular_velocity.y = float(msg.gyro_rad[1])
        imu_msg.angular_velocity.z = float(msg.gyro_rad[2])

        # Linear acceleration from accelerometer
        imu_msg.linear_acceleration.x = float(msg.accelerometer_m_s2[0])
        imu_msg.linear_acceleration.y = float(msg.accelerometer_m_s2[1])
        imu_msg.linear_acceleration.z = float(msg.accelerometer_m_s2[2])

        # Orientation is unknown here, so set zero quaternion
        imu_msg.orientation.x = 0.0
        imu_msg.orientation.y = 0.0
        imu_msg.orientation.z = 0.0
        imu_msg.orientation.w = 1.0

        # Optional: set covariance matrices to unknown (-1) or zeros
        imu_msg.orientation_covariance = [
            0.01, 0.0, 0.0,
            0.0, 0.01, 0.0,
            0.0, 0.0, 0.01
        ]
        imu_msg.angular_velocity_covariance = [
            0.0008726646**2, 0.0, 0.0,
            0.0, 0.0008726646**2, 0.0,
            0.0, 0.0, 0.0008726646**2
        ]

        imu_msg.linear_acceleration_covariance = [
            0.00637**2, 0.0, 0.0,
            0.0, 0.00637**2, 0.0,
            0.0, 0.0, 0.00686**2
        ]

        self.pub.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorCombinedToImu()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
