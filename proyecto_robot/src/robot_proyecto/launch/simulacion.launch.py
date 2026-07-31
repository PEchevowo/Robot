import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # rutas de los archivos
    paquete = 'robot_proyecto'
    ruta_paquete = get_package_share_directory(paquete)
    ruta_modelo = os.path.join(ruta_paquete, 'urdf', 'robot.urdf.xacro')

    # procesar el archivo xacro
    doc_xml = xacro.process_file(ruta_modelo)
    robot_desc = {'robot_description': doc_xml.toxml()}

    # nodo para publicar el estado del robot (¡Añadido use_sim_time!)
    nodo_estado = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_desc, {'use_sim_time': True}]
    )

    # arrancar el simulador con el mundo de paredes
    ruta_mundo = os.path.join(ruta_paquete, 'worlds', 'mundo_paredes.sdf')
    ruta_gazebo = get_package_share_directory('ros_gz_sim')
    lanzar_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ruta_gazebo, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'{ruta_mundo} -r'}.items()
    )

    # inyectar el robot en el simulador
    nodo_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'robot_diferencial'],
        output='screen'
    )

    # nodo puente para conectar los datos de ros 2 con gazebo
    nodo_puente = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',  # <-- ¡Reloj virtual añadido aquí!
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
        output='screen'
    )

    # nodo para publicar la transformacion de odom a base_footprint (¡Añadido use_sim_time!)
    nodo_odom_tf = Node(
        package='robot_proyecto',
        executable='odom_tf_publisher',
        name='odom_tf_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        nodo_estado,
        lanzar_gazebo,
        nodo_spawn,
        nodo_puente,
        nodo_odom_tf,
    ])