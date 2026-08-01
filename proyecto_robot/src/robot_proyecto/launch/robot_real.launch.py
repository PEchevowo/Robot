from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Nodo del LiDAR Hokuyo
        Node(
            package='urg_node',
            executable='urg_node_driver',
            name='urg_node',
            parameters=[{
                'serial_port': '/dev/ttyACM0',
                'frame_id': 'laser_frame',
                'angle_min': -2.35,
                'angle_max': 2.35
            }]
        ),
        # 2. Nodo del puente serial (Músculos)
        Node(
            package='robot_proyecto',
            executable='serial_bridge',
            name='serial_bridge'
        ),
        # 3. Nodo de Odometría (Cálculo de movimiento)
        Node(
            package='robot_proyecto',
            executable='odom_tf_publisher',
            name='odom_tf_publisher'
        ),
        # 4. Transformada física (Une el láser al chasis del robot)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_laser',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser_frame']
        )
    ])