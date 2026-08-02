import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        # ajusta el puerto segun como la jetson reconozca al arduino
        self.puerto = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.mover, 10)

    def mover(self, msg):
        lineal = msg.linear.x * 5
        angular = msg.angular.z
        
        # enviamos los datos separados por coma
        comando = f"{lineal},{angular}\n"
        self.puerto.write(comando.encode('utf-8'))

def main(args=None):
    rclpy.init(args=args)
    nodo = SerialBridge()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()