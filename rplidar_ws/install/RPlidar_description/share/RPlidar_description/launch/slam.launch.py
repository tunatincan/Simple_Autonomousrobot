import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paths to the package and config
    pkg_share = get_package_share_directory('RPlidar_description')
    slam_config_file = os.path.join(pkg_share, 'config', 'mapper_params_online_async.yaml')

    # SLAM Toolbox Node
    start_async_slam_toolbox_node = Node(
        parameters=[
          slam_config_file,
          {'use_sim_time': True}
        ],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen'
    )

    return LaunchDescription([
        start_async_slam_toolbox_node
    ])
