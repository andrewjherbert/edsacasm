# Transfer EDSAC tank 0 images to SSI  - Andrew Herbert 29/07/2021

import argparse
import serial
import sys
import time

# ---- ssiUpload ---- #

def ssiUpload (inFilePath, devicePath):

    # Set up serial port
    ser = serial.Serial()
    ser.port     = devicePath
    ser.baudrate = 38400

    # Open serial port
    try:
        ser.open()
    except serial.SerialException as e:
            sys.stderr.write(
                'Could not open serial port {}: {}\n'.format(ser.name, e))
            sys.exit(1)

    # Read  file
    with open(inFilePath) as infile:
        buf = (infile.read()).encode('ascii') # force input to ASCII
    # Send file to SSI
    ssiSend(buf, ser)

    # Close the serial port
    ser.close()

# ---- ssiSend ---- #

def ssiSend(buf, ser):
    for ch in buf:
        # echo any messages coming back
        while ser.in_waiting > 0:
            b = ser.read (1)
            print(chr(b[0]), end="")

            # Output character to punch
            while ser.out_waiting > 0:
                time.sleep (0.001)
            if ser.write (bytes([ch]))  != 1:
                sys.stderr.write("ser.write failed\n")
                sys.exit(1)

# ---- main program ---- #

print("Start")
parser = argparse.ArgumentParser(
description='Transfer tank 0 image via SSI')
parser.add_argument('-device',  help='serial device', default='')
parser.add_argument('-infile',  help='input file', default='')
args = parser.parse_args()
inFilePath = args.infile
devicePath = args.device
ssiUpload(inFilePath, devicePath)
