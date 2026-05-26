import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')

        self.publisher_ = self.create_publisher(
            Float32,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.5,
            self.timer_callback
        )

        self.speed = 0.0

    # Bug 1 fix:
    # Timer callbacks in ROS 2 do not accept message arguments,
    # so the extra 'msg' parameter was removed.
    def timer_callback(self):

        self.speed += 0.1

        msg = Float32()
        msg.data = self.speed

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing: {msg.data}'
        )


def main():

    rclpy.init()

    node = VelocityPublisher()

    # Bug 2 fix:
    # rclpy.spin() must receive the node object
    # so ROS 2 can execute its callbacks.
    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()


# Explanation:
# This ROS 2 node creates a publisher that sends Float32 values
# to the /cmd_vel topic. A timer runs every 0.5 seconds and calls
# timer_callback(), where the velocity value increases by 0.1 and
# gets published. rclpy.spin(node) keeps the node active and allows
# the timer callback to execute repeatedly until the program stops.