import rclpy
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import GPSRAW
import csv

class MiNodoSuscriptor:

    def __init__(self):
        self.node = rclpy.create_node('mi_nodo_suscriptor')
        self.subscription = self.node.create_subscription(
            GPSRAW,
            '/rpsc2/gpsstatus/gps1/raw',
            self.callback,
            10
        )
        self.csv_file = open('gps_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Frame ID', 'Fix Type', 'Latitud', 'Longitud', 'Altitud'])
        self.node.get_logger().info('Nodo suscriptor iniciado')

    def callback(self, msg):
        try:
            stamp = msg.header.stamp
            frame_id = msg.header.frame_id
            fix_type = msg.fix_type
            lat = msg.lat
            lon = msg.lon
            alt = msg.alt

            self.node.get_logger().info(f'Stamp: {stamp.sec}.{stamp.nanosec}, Frame ID: {frame_id}, '
                                        f'Fix Type: {fix_type}, Latitud: {lat}, Longitud: {lon}, Altitud: {alt}')

            # Escribir los datos al archivo CSV
            self.csv_writer.writerow([f'{stamp.sec}.{stamp.nanosec}', frame_id, fix_type, lat, lon, alt])

        except Exception as e:
            self.node.get_logger().error(f'Error al procesar el mensaje: {e}')

    def destroy_node(self):
        try:
            self.csv_file.close()
        except Exception as e:
            self.node.get_logger().error(f'Error al cerrar el archivo CSV: {e}')
        finally:
            super().destroy_node()

def main(args=None):
    rclpy.init(args=args)

    mi_nodo_suscriptor = MiNodoSuscriptor()

    try:
        rclpy.spin(mi_nodo_suscriptor.node)
    except KeyboardInterrupt:
        mi_nodo_suscriptor.node.get_logger().info('Nodo detenido manualmente')
    finally:
        mi_nodo_suscriptor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

