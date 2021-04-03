#!/usr/bin/env python3

import logging

import adafruit_bno055
import board
import busio

import click

import yaml

from time import sleep

from networktables import NetworkTables

logging.basicConfig(level=logging.INFO)

def set_calibration_data(calibration_file, bno):
    calibration_data = {}
     
    with open(calibration_file, "r") as f:
        calibration_data = yaml.safe_load(f)

    bno.mode = adafruit_bno055.CONFIG_MODE

    bno.offsets_accelerometer = (
            calibration_data['accelerometer_offsets']['x'],
            calibration_data['accelerometer_offsets']['y'],
            calibration_data['accelerometer_offsets']['z']
        )
    bno.offsets_gyroscope = (
            calibration_data['gyroscope_offsets']['x'],
            calibration_data['gyroscope_offsets']['y'],
            calibration_data['gyroscope_offsets']['z']
        )
    bno.offsets_magnetometer = (
            calibration_data['magnetometer_offsets']['x'],
            calibration_data['magnetometer_offsets']['y'],
            calibration_data['magnetometer_offsets']['z']
        )
    bno.radius_accelerometer = calibration_data['accelerometer_radius']
    bno.radius_magnetometer = calibration_data['magnetometer_radius']

    bno.mode = adafruit_bno055.NDOF_MODE

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
    if acceleration and None not in acceleration:
        table.putNumber("accel_x", acceleration[0])
        table.putNumber("accel_y", acceleration[1])
        table.putNumber("accel_z", acceleration[2])

    # Put magnetic
    if magnetic and None not in magnetic:
        table.putNumber("mag_x", magnetic[0])
        table.putNumber("mag_y", magnetic[1])
        table.putNumber("mag_z", magnetic[2])

    # Put gyro
    if gyro and None not in gyro:
        table.putNumber("gyro_x", gyro[0])
        table.putNumber("gyro_y", gyro[1])
        table.putNumber("gyro_z", gyro[2])

    # Put euler
    if euler and None not in euler:
        table.putNumber("euler_yaw", euler[0])
        table.putNumber("euler_roll", euler[1])
        table.putNumber("euler_pitch", euler[2])

    # Put quaternion
    if quaternion and None not in quaternion:
        table.putNumber("quat_x", quaternion[0])
        table.putNumber("quat_y", quaternion[1])
        table.putNumber("quat_z", quaternion[2])
        table.putNumber("quat_w", quaternion[3])

    # Put linear acceleration
    if linear_acceleration and None not in linear_acceleration:
        table.putNumber("lin_accel_x", linear_acceleration[0])
        table.putNumber("lin_accel_y", linear_acceleration[1])
        table.putNumber("lin_accel_z", linear_acceleration[2])

    # Put gravity
    if gravity and None not in gravity:
        table.putNumber("gravity_x", gravity[0])
        table.putNumber("gravity_y", gravity[1])
        table.putNumber("gravity_z", gravity[2])

@click.command()
@click.option("--calibration", help="Path to the calibration yaml file from calibrate_bno.py.")
@click.option("--net-tables-server", default="roborio-3786-frc.local",
              help="The server IP for the Network Tables server.")
def main(calibration, net_tables_server):
    """Output data from the BNO to Network Tables
    """
    logging.info("Starting network tables...")
    NetworkTables.initialize(server=net_tables_server)

    while not NetworkTables.isConnected():
        logging.info("Waiting for Network Tables to connect...")
        sleep(1)

    bno_table = NetworkTables.getTable("BNO055")
    logging.info("Connecting to BNO...")
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    if calibration:
        set_calibration_data(calibration, sensor)

    logging.info("Initialization complete.")

    try:
        while True:
            write_bno_to_network_table(bno_table, sensor)
    except KeyboardInterrupt:
        logging.error("Interrupted!")

    NetworkTables.shutdown()


if __name__ == "__main__":
    main()
