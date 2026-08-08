import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from my_robot_interfaces.msg import DetectObject

class SubscriberNode(Node) :

    def __init__(self):

        super().__init__("subscriber")

    # create subscription takes a msg type, topic name, callback function and queue size as input and returns a subscription object
    
        self.subscription = self.create_subscription(
            String,
            "/chat",
            self.message_callback,
            10
        )

    # creating a new subscriber for custom interface msg publisher
        self.subscription = self.create_subscription(
            DetectObject,
            "/detected_object",
            self.custom_interface_callback,
            10
        )

    def message_callback(self, message):

        self.get_logger().info(
            f'Recieved : "{message.data}"'
        )

    def custom_interface_callback(self, message):
        self.get_logger().info(
            f'Recieved Custom Message : "{message}"'
        )


def main(args=None):
    rclpy.init(args=args)

    node = SubscriberNode()

    rclpy.spin(node)

    rclpy.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__" :
    main()