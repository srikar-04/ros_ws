import rclpy
from rclpy.node import Node

from my_robot_interfaces.srv import SetGripper

class GripperClient(Node):
    def __init__(self):
        super().__init__("gripper_client")

        # takes interface and service name (name that we give to service while creating it using create_service function) as arguments 

        self.gripper_client = self.create_client(
            SetGripper,
            "/set_gripper"
        )

        while not self.gripper_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Waiting for /set_gripper service..."
            )


    def send_request(self, open_gripper):
        request = SetGripper.Request()

        request.open = open_gripper

        # A service request can take time to execute. we should not block the entire node until we get a response from service. (Because remember that a node can contain multiple publishers and subscribers. if we do a sync call, all others will get blocked)

        # the call_async function immediately returns a "Future" object which does not contain any response intitially. (it is just like javascript returning promoise object before fetching response). Once DDS delivers the response, the future object will get completed

        future = self.gripper_client.call_async(request)

        return future


def main(args=None):

    rclpy.init(args=args)

    node = GripperClient()

    future = node.send_request(True)

    # This tells the executor to continue processing events until we future object is complete

    rclpy.spin_until_future_complete(
        node,
        future
    )

    # we get the response object here (SetGripper.Response)
    response = future.result()

    node.get_logger().info(
        f"Success : {response.success}, \n"
        f"Messaage: {response.message}"
    )

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__" :
    main()