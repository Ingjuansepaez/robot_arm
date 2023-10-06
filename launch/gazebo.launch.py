#Librerias para Ubicar Archivos
import os
from ament_index_python import get_package_share_directory
#Librerias para Lanzar Nodos
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch import LaunchDescription

pkg_share_filepath= os.path.join(get_package_share_directory("robot_arm"))
rsp_launch_filepath= os.path.join(pkg_share_filepath, "launch", "rs_publisher.launch.py")
urdf_filepath= os.path.join(pkg_share_filepath, "urdf", "robot_arm.urdf.xacro")

def generate_launch_description():
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_launch_filepath]),
        launch_arguments= {
            'use_sim_time': 'true',
            'use_ros2_control': 'true'
        }.items()
    )
    
    gazebo_cmd = ExecuteProcess(
        cmd= ["gazebo","-s","libgazebo_ros_factory.so"],
        output= "screen",
    )
    
    gazebo_spawner_node = Node(
        package = "gazebo_ros",
        executable = "spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'brazo'],
    )

    nodes_to_run = [rsp_launch, gazebo_cmd, gazebo_spawner_node]
    return LaunchDescription(nodes_to_run)
       