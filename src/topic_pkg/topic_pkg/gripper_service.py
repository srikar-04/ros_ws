import rclpy
from rclpy.node import Node

from my_robot_interfaces.srv import SetGripper

class GripperService(Node):
    def __init__(self):
        super().__init__("gripper_service")

        self.gripper_service = self.create_service(
            SetGripper,
            "/set_gripper",
            self.handle_gripper
        )

        self.get_logger().info(
            "Gripper Service is Ready"
        )

    def handle_gripper(self, request, response):

        if request.open:
            response.success = True
            response.message = "Gripper Opened"
        else :
            response.success = False
            response.message = "Gripper Closed"

        return response

def main(args=None):
    rclpy.init(args=args)

    node = GripperService()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__" :
    main()