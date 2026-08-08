import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from my_robot_interfaces.action import MoveRobot

import time

from rclpy.executors import MultiThreadedExecutor

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
            callback_group=self.callback_group
        )

        self.get_logger().info(
            "Move Robot Action Server Is Ready"
        )

    # This is not a normal callback like topic or service. It is a goal callback, it recieves goal_handle which respresents the particular goal sent by the client

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target

        self.get_logger().info(
            f"Recieved goal : {target}"
        )

        feedback = MoveRobot.Feedback()

        rate = self.create_rate(1.0) # 1.0 Hz = 1 second loop

        for i in range(1, 11):
            # time.sleep(1) -> This is blocking the single threaded executor. we are not using this

            feedback.progress = float(i*10)

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f"Progress : {feedback.progress}%"
            )

            rate.sleep()
        goal_handle.succeed()

        result = MoveRobot.Result()

        result.success = True

        self.get_logger().info(
            "Goal Completed"
        )

        return result

def main(args=None):
    rclpy.init(args=args)

    node = MoveRobotServer()

    # we are using multi-thread executor here, we may or may not use it in future.

    executor = MultiThreadedExecutor()

    executor.add_node(node)

    try :
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally :

        node.destroy_node()

        rclpy.shutdown()

if __name__ == "__main__" :
    main()