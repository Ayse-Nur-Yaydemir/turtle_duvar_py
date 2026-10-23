import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleDuvarNode(Node):
    def __init__(self):
        super().__init__('turtle_duvar_node')
        
        
        self.declare_parameter('linear_speed', 2.0)
        self.declare_parameter('angular_speed', 2.5)
        self.declare_parameter('min_limit', 1.5)
        self.declare_parameter('max_limit', 9.5)
        
       
        self.x = 0.0
        self.y = 0.0
        
        
        self.pose_subscriber = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
       
        self.cmd_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        
       
        self.timer = self.create_timer(0.1, self.control_loop)
        
       
        self.log_timer = self.create_timer(1.0, self.log_status)

    def pose_callback(self, msg: Pose):
        self.x = msg.x
        self.y = msg.y

    def control_loop(self):
        msg = Twist()
        
        
        lin_speed = self.get_parameter('linear_speed').value
        ang_speed = self.get_parameter('angular_speed').value
        min_val = self.get_parameter('min_limit').value
        max_val = self.get_parameter('max_limit').value
        
        
        if self.x < min_val or self.x > max_val or self.y < min_val or self.y > max_val:
            msg.linear.x = lin_speed * 0.5   # Duvardan uzaklaşırken hafif ileri hız
            msg.angular.z = ang_speed        # Açısal hız
        else:
            msg.linear.x = lin_speed         # Normal düz sürüş hızı
            msg.angular.z = 0.0
            
        self.cmd_publisher.publish(msg)

    def log_status(self):
        
        lin_speed = self.get_parameter('linear_speed').value
        min_val = self.get_parameter('min_limit').value
        max_val = self.get_parameter('max_limit').value
        
        self.get_logger().info(
            f'Konum -> X: {self.x:.2f}, Y: {self.y:.2f} | '
            f'Hız: {lin_speed}, Sınırlar: [{min_val}, {max_val}]'
        )

def main(args=None):
    rclpy.init(args=args)
    node = TurtleDuvarNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
