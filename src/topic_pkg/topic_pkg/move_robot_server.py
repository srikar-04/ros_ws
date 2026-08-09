import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from my_robot_interfaces.action import MoveRobot

import time


class MoveRobotServer(Node):
    def __init__(self):
        super().__init__("move_robot_server")

        # Action server is an api provided by ros2
        # It takes 
            # self, 
            # an action interface (MoveRobot in our case),
            # an action name (/move_robot in our case) and 
            # a callback function to execute to handle goal
        self.robot_action_server = ActionServer(
            self,
            MoveRobot,
            "/move_robot",
            self.execute_callback,
        )

        self.get_logger().info(
            "Move Robot Action Server Is Ready"
        )

    # This is not a normal callback like topic or service. It is a goal callback, it recieves goal_handle which respresents the particular goal/target sent by the client and it is also capable of sending feedback and cancellation response to client. One the goal is completed, it can also send result to client.

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target

        self.get_logger().info(
            f"Recieved goal : {target}"
        )

        feedback = MoveRobot.Feedback()

        for i in range(1, 11):

            time.sleep(1)

            if goal_handle.is_cancel_requested:

                self.get_logger().info(
                    "Cancellation requested."
                )
                
                # This tells ros that i have accepted cancellation request and the gaol is now cancelled

                goal_handle.canceled()

                result = MoveRobot.Result()
                result.success = False

                return result

            feedback.progress = float(i * 10)

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f"Progress: {feedback.progress}%"
            )

            # rate.sleep()
        goal_handle.succeed()

        result = MoveRobot.Result()
        result.success = True

        self.get_logger().info(
            "Goal completed."
        )

        return result

def main(args=None):
    rclpy.init(args=args)

    node = MoveRobotServer()

    rclpy.spin(node)
    
    node.destroy_node()

    rclpy.shutdown()
if __name__ == "__main__" :
    main()