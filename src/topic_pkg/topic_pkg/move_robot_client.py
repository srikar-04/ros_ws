import rclpy
from rclpy.node import Node

from my_robot_interfaces.action import MoveRobot

from rclpy.action import ActionClient

class MoveRobotClient(Node):
    def __init__(self):
        super().__init__('move_robot_client')

        self.action_client = ActionClient(
            self,
            MoveRobot,
            "/move_robot"
        )

        self.goal_handle = None
        self.cancel_timer = None

    def send_goal(self, target) :
        self.get_logger().info(
            f"Waiting for /move_robot action server..."
        )

        # The client waits for DDS to find appropriate server based on our action and interface

        self.action_client.wait_for_server()

        self.get_logger().info(
            f"Sneding goal : {target}"
        )

        # creates an object for the Goal section of our interface
        goal = MoveRobot.Goal()

        goal.target = target

        # we are asking ros to send goal to server but we are not waiting for the entire process to finish. we are doing this asynchronously 
        send_goal_future = self.action_client.send_goal_async(
            goal,
            feedback_callback = self.feedback_callback
        )

        # when the future eventually gets completed and we get a result, ros executes the goal_response_callback 
        send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future) :
        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().info(
                "Goal was rejected"
            )
            return 
        
        self.get_logger().info(
            "Goal Accepted"
        )

        self.get_logger().info(
            f"Goal ID: {self.goal_handle.goal_id.uuid}"
        )

        self.cancel_timer = self.create_timer(
            3.0,
            self.cancel_goal
        )

        result_future = self.goal_handle.get_result_async()

        result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_message):

        feedback = feedback_message.feedback

        self.get_logger().info(
            f"Progress: {feedback.progress}%"
        )

    def cancel_goal(self):
        if self.cancel_timer is not None:
            self.cancel_timer.cancel()

        if self.goal_handle is None:
            return
        
        self.get_logger().info(
            "Sending cancellation request"
        )

        cancel_future = self.goal_handle.cancel_goal_async()

        cancel_future.add_done_callback(
            self.cancel_response_callback
        )

    def cancel_response_callback(self, future):
        cancel_response = future.result()

        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info(
                "Cancel accepted by server"
            )
        else :
            self.get_logger().info(
                "Cancellation rejected by server"
            )

    def result_callback(self, future):

        result = future.result()

        self.get_logger().info(
            f"Result stauts: {result.status}"
        )

        self.get_logger().info(
            f"Result success : {result.result.success}"
        )

        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    node = MoveRobotClient()

    node.send_goal(10.0)

    rclpy.spin(node)


if __name__ == "__main__" :
    main()