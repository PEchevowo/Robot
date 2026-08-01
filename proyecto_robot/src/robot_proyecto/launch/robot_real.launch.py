from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Nodo del LiDAR Hokuyo
        Node(
            package='urg_node',
            executable='urg_node_driver',
            name='urg_node',
            parameters=[{
                'serial_port': '/dev/ttyACM0', # Cambiar a ACM0 o ACM1 según corresponda
                'frame_id': 'laser_frame',
                'angle_min': -2.35, # Los Hokuyo suelen tener mayor apertura
                'angle_max': 2.35
            }]
        ),
        # Nodo del puente serial para mover los motores vía Arduino
        Node(
            package='robot_proyecto',
            executable='serial_bridge',
            name='serial_bridge'
        )
    ])