#!/usr/bin/env python3

import logging
import click

import adafruit_bno055
import board
import busio

import yaml

from time import sleep

logging.basicConfig(level=logging.INFO)

def print_status(bno):
    sys_status, g_status, a_status, m_status = bno.calibration_status
    logging.info("Status (3 == complete):\n\tSys: {}\n\tG: {}\n\tA: {}\n\tG: {}".format(sys_status,
                                                                                        g_status,
                                                                                        a_status,
                                                                                        m_status))

def output_calibration_data(output_file, bno):
    logging.info("Calibration offsets:")
    logging.info("\tAccelerometer: {}".format(bno.offsets_accelerometer))
    logging.info("\tGyroscope: {}".format(bno.offsets_gryoscope))
    logging.info("\tMagnetometer: {}".format(bno.offsets_magnetometer))
    logging.info("\tAccelerometer Radius: {}".format(bno.radius_accelerometer))
    logging.info("\tMagnetometer Radius: {}".format(bno.radius_magnetometer))

    output_data = {
        'accelerometer_offsets': bno.offsets_accelerometer,
        'gryoscope_offsets': bno.offsets_gryoscope,
        'magnetometer_offsets': bno.offsets_magnetometer,
        'accelerometer_radius': bno.radius_accelerometer,
        'magnetometer_radius': bno.radius_magnetometer
    }

    with open(output_file, "r") as f:
        yaml.dump(output_data, f)

@click.command()
@click.option("--output-file", help="File to output calibration to.")
def main(output_file):
    logging.info("Connecting to BNO...")
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    sensor.mode = adafruit_bno055.NDOF_MODE

    logging.info("Starting calibration...")
    while not sensor.calibrated:
        print_status(sensor)
        sleep(0.5)

    output_calibration_data(output_file, sensor)

if __name__ == "__main__":
    main()
