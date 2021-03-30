#!/usr/bin/env python3

import logging

import adafruit_bno055
import board
import busio

from networktables import NetworkTables

logging.basicConfig(level=logging.DEBUG)

def write_bno_to_network_table(table, bno):
    # Gather data from BNO to avoid drift while writing to tables
    acceleration = bno.acceleration
    magnetic = bno.magnetic
    gyro = bno.gyro
    euler = bno.euler
    quaternion = bno.quaternion
    linear_acceleration = bno.linear_acceleration
    gravity = bno.gravity

    # Skip temperature for now

    # Put acceleration
    table.putNumber("accel_x", acceleration[0]) if acceleration[0]
    table.putNumber("accel_y", acceleration[1]) if acceleration[0]
    table.putNumber("accel_z", acceleration[2]) if acceleration[0]

    # Put magnetic
    table.putNumber("mag_x", magnetic[0]) if magnetic[0]
    table.putNumber("mag_y", magnetic[1]) if magnetic[0]
    table.putNumber("mag_z", magnetic[2]) if magnetic[0]

    # Put gyro
    table.putNumber("gyro_x", gyro[0]) if gyro[0]
    table.putNumber("gyro_y", gyro[1]) if gyro[0]
    table.putNumber("gyro_z", gyro[2]) if gyro[0]

    # Put euler
    table.putNumber("euler_roll", euler[0]) if euler[0]
    table.putNumber("euler_pitch", euler[1]) if euler[0]
    table.putNumber("euler_yaw", euler[2]) if euler[0]

    # Put quaternion
    table.putNumber("quat_x", quaternion[0]) if quaternion[0]
    table.putNumber("quat_y", quaternion[1]) if quaternion[0]
    table.putNumber("quat_z", quaternion[2]) if quaternion[0]
    table.putNumber("quat_w", quaternion[3]) if quaternion[0]

    # Put linear acceleration
    table.putNumber("lin_accel_x", linear_acceleration[0]) if linear_acceleration[0]
    table.putNumber("lin_accel_y", linear_acceleration[1]) if linear_acceleration[0]
    table.putNumber("lin_accel_z", linear_acceleration[2]) if linear_acceleration[0]

    # Put gravity
    table.putNumber("gravity_x", gravity[0]) if gravity[0]
    table.putNumber("gravity_y", gravity[1]) if gravity[0]
    table.putNumber("gravity_z", gravity[2]) if gravity[0]

def main():
    logging.info("Starting network tables...")
    NetworkTables.initialize()
    bno_table = NetworkTables.getTable("BNO055")
    logging.info("Connecting to BNO...")
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    logging.info("Initialization complete.")

    try:
        while True:
            write_bno_to_network_table(bno_table, sensor)
    except KeyboardInterrupt:
        logging.error("Interrupted!")

    NetworkTables.shutdown()


if __name__ == "__main__":
    main()
