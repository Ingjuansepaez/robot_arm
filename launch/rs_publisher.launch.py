#Librerias para Ubicar Archivos
import os
from ament_index_python import get_package_share_directory
#Librerias para Procesar Archivos
import xacro
#Librerias para Lanzar Nodos
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument

pkg_share_filepath = os.path.join(get_package_share_directory("robot_arm"))
urdf_filepath = os.path.join(pkg_share_filepath, "urdf", "robot_arm.urdf.xacro")

use_sim_time = LaunchConfiguration("use_sim_time")
use_ros2_control = LaunchConfiguration('use_ros2_control')
robot_description = Command(['xacro ', urdf_filepath, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])

def generate_launch_description():
    use_sim_time_declaration = DeclareLaunchArgument(
        "use_sim_time", 
        default_value= "true", 
        description= "Use sim time if true"
    )

    use_ros2_control_declaration = DeclareLaunchArgument(
        'use_ros2_control',
        default_value='true',
        description='Use ros2_control if true'
    )

    rsp_node = Node(
        package= "robot_state_publisher",
        executable= "robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time
            }
        ]
    )

    nodes_to_run = [use_sim_time_declaration, use_ros2_control_declaration, rsp_node]
    return LaunchDescription(nodes_to_run)
