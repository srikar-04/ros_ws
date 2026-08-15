import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from my_robot_interfaces.action import MoveRobot

import time


class MoveRobotServer(Node):
    def __init__(self):
        super().__init__("move_robot_server")

        self.callback_group = ReentrantCallbackGroup()

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
            execute_callback = self.execute_callback,
            goal_callback = self.goal_callback,
            cancel_callback = self.cancel_callback,
            callback_group = self.callback_group
        )

        self.get_logger().info(
            "Move Robot Action Server Is Ready"
        )

    # goal_callback and cancel_callbakc are merly used for accepting and rejecting respecitve goals and cacellation requests

    # When client gives a goal/target to server, the control first reaches the goal_callback. goal_callback has the authority to accept or reject the goal. If the goal is accepted by goal_callback then the control reaches to execute callback where the actual execution happens based on the target sent by client. 

    # If there is no goal_callback, ROS2 by default accepts all the incoming goals
    def goal_callback(self, goal_request) :

        self.get_logger().info(
            f"Revieved goal request : {goal_request.target}"
        )

        return GoalResponse.ACCEPT

    # When there is a cancellation request, it first reaches the cancel_callback, this callback has the ability to either accept or reject the cancellation request. If cancellation request is accepted then the if condition with "is_handle_requested" becomes true in the execution callback.
    def cancel_callback(self, cancel_request):
        self.get_logger().info(
            f"Recieved cancellation request"
        )

        return CancelResponse.ACCEPT

    # IMPORTANT : So these goal and cancel callbacks are just decision callbacks, they do not perform any execution. Execution is done inside exection callback

    # This is not a normal callback like topic or service. It is a goal callback, it recieves goal_handle which respresents the particular goal/target sent by the client and it is also capable of sending feedback response to client. Once the goal is completed, it can also send result to client. 

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target

        self.get_logger().info(
            f"Executing goal : {target}"
        )

        feedback = MoveRobot.Feedback()
        result = MoveRobot.Result()

        for i in range(1, 11):

            if goal_handle.is_cancel_requested:

                self.get_logger().info(
                    "Cancellation requested. Stopping Goal"
                )
                
                # This tells ros that i have accepted cancellation request and the gaol is now cancelled

                goal_handle.canceled()

                result.success = False

                self.get_logger().info(
                    f"Goal Canceled"
                )

                return result

            feedback.progress = float(i * 10)

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f"Progress: {feedback.progress}%"
            )

            time.sleep(1)

            # rate.sleep()
        goal_handle.succeed()

        result.success = True

        self.get_logger().info(
            "Goal completed."
        )

        return result

def main(args=None):
    rclpy.init(args=args)

    node = MoveRobotServer()

    executor = MultiThreadedExecutor(
        num_threads=2
    )

    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

    rclpy.shutdown()
if __name__ == "__main__" :
    main()