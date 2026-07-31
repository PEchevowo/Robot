import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    paquete = get_package_share_directory('robot_proyecto')
    ruta_urdf = os.path.join(paquete, 'urdf', 'robot.urdf.xacro')
    
    # Procesar el archivo modelo
    doc_xacro = xacro.process_file(ruta_urdf)
    desc_robot = doc_xacro.toxml()
    
    # Nodo para publicar el estado de las piezas del robot
    nodo_estado = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': desc_robot}]
    )
    
    # Nodo para abrir la interfaz gráfica
    nodo_rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )
    
    return LaunchDescription([
        nodo_estado,
        nodo_rviz
    ])