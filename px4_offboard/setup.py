import os
from glob import glob
from setuptools import setup

package_name = 'px4_offboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/ament_index/resource_index/packages',
            ['resource/' + 'visualize.rviz']),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
        (os.path.join('share', package_name), glob('resource/*rviz'))
        # (os.path.join('share', package_name), ['scripts/TerminatorScript.sh'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Braden',
    maintainer_email='braden@arkelectron.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
                'offboard_control = px4_offboard.offboard_control:main',
                'visualizer = px4_offboard.visualizer:main',
                'velocity_control = px4_offboard.velocity_control:main',
                'control = px4_offboard.control:main',
                'processes = px4_offboard.processes:main',
                'imu_extract = px4_offboard.imu_extract:main',
                'pointcloud_filter = px4_offboard.pointcloud_filter:main',
                'odom_tf_publisher = px4_offboard.odom_tf_publisher:main',
                'odom_to_path = px4_offboard.odom_to_path:main',
                'lidar_timefix = px4_offboard.lidar_timefix:main',
                'cartographer_pose = px4_offboard.cartographer_pose:main'
                ],
    },
)
