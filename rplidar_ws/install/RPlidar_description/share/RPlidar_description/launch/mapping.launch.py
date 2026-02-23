import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('RPlidar_description')

    # 1. Include the gazebo launch file (which spawns the world and robot)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Include the SLAM Toolbox launch file
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'slam.launch.py')
        )
    )

    # 3. Start RViz2 with use_sim_time
    # We use ExecuteProcess to pass the specific command line arguments easily
    rviz_node = ExecuteProcess(
        cmd=['rviz2', '--ros-args', '-p', 'use_sim_time:=true'],
        output='screen'
    )

    # 4. Start the teleop keyboard node in a new terminal window automatically
    # Requires gnome-terminal, which is standard on Ubuntu
    teleop_node = ExecuteProcess(
        cmd=['gnome-terminal', '--', 'bash', '-c', 'ros2 run teleop_twist_keyboard teleop_twist_keyboard; exec bash'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        slam_launch,
        rviz_node,
        teleop_node
    ])
