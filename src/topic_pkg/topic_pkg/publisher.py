import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from my_robot_interfaces.msg import DetectObject

# rclpy is ros2 python client library. It acts as a bridge between actual python code logic and ros2 framework. 
# other smart devs has already created some code logic for us on almost every important aspect of ros2. we can use those code logic by importing them and build our application on top of it. 
# so rclpy makes our life easier by providing us with pre-built code logic for ros2.

class PublisherNode(Node):

    # when we call this constructor, we are telling the "Node" class to initialize itself and after that initialize a node with name "publisher".
    # the Node class is a base class for all ros2 nodes. It contains thousand of lines describing how ros2 nodes should behave and communicate with each other
    def __init__(self):
        super().__init__("publisher")


        self.publisher = self.create_publisher(
            String,
            "/chat",
            10
        )

        self.count = 0

        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

        # creating a second publisher for sending custom message

        self.object_pub = self.create_publisher(
            DetectObject,
            "/detected_object",
            10
        )

        # creating a second timer for custom message publisher

        self.interface_timer = self.create_timer(
            2.0,
            self.publish_interface_messaage
        )

    def publish_message(self) :

        msg = String()

        msg.data = f"Message {self.count}"
        
        self.publisher.publish(msg)

        self.get_logger().info(
            f"Published: \"{msg.data}\""
        )
        self.count+=1

    # sending a custom message to subscriber
    def publish_interface_messaage(self) :
        msg = DetectObject()

        msg.name = "srikar"
        # msg.confidence = float(0.94)
        # msg.x = float(320.0)
        # msg.y = float(180.0)
        msg.confidence = 0.94
        msg.x = 320.0
        msg.y = 180.0

        self.object_pub.publish(msg)
        self.get_logger().info(
            f"Published Custom Message: \"{msg}\""
        )


def main(args=None):
    rclpy.init(args=args)

    node = PublisherNode()

    # rclpy.spin() is a function that keeps the node alive and responsive to incoming messages and events.
    # IMPORTANT : this function creates a callback loop, just like javascript. It executes the callback functions whenever a message is recieved or when you write any callback function.
    # If we remove this function, node will end almost immediately after it is created and we will not be able to see any output from the node.
    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()