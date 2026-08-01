from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Nodo del LiDAR Hokuyo (Con el nombre de frame corregido)
        Node(
            package='urg_node',
            executable='urg_node_driver',
            name='urg_node',
            parameters=[{
                'serial_port': '/dev/ttyACM0',
                'frame_id': 'laser', 
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
        # 3. Transformada física (Une el láser al chasis del robot)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_laser',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser']
        ),
        # 4. Odometría Fija (Puente matemático para Nav2 y SLAM)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odom_to_base',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link']
        )
    ])