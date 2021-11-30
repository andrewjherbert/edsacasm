
#Transfer EDSAC tank 0 images to SSI  - Andrew Herbert 19/10/2021

# ssiupload device infile

import argparse
import serial
import sys
import time

# ---- ssiUpload ---- #

def ssiUpload (filePath, devicePath):

    # Set up serial port
    ser = serial.Serial()
    ser.port     = devicePath
    ser.baudrate = 38400

    # Open serial port
    try:
        print("Opening", devicePath)
        ser.open()
    except serial.SerialException as e:
            sys.stderr.write(
                'ssiupload: Could not open serial port {}: {}\n'.format(ser.name, e))
            sys.exit(1)

    # Read  file
    file = None
    try:
        file = open(filePath, 'rt')
    except:
        print("Cannot open input file")
        sys.exit(1)
    buf = (file.read()).encode('ascii') # force input to ASCII

    # Set up SSI unit
    input("SSI unit should have reset, type RETURN to continue")
    input("Select LOCAL mode and type RETURN to continue")
    input("Scroll to, but do not select, TEXTFILE and type RETURN to continue")
    
    # Send file to SSI
    ssiSend(buf, ser)

    ssiEcho(ser) # clear any output from SSI

    print("Select TEXTFILE to load copy to store")

    ssiWait()  # clear any output from SSI
    ssiEcho(ser)

    input("Type RETURN to exit from ssiupload")

    # Close the serial port
    ser.close()

# ---- ssiWait ----#

def ssiWait(ser):
    print("Waiting for SSI input");
    while ser.in_waiting == 0:
        time.sleep(0.1)
        
# ---- ssiEcho ---- #

def ssiEcho(ser):
    # echo any messages coming back
    print("Looking for SSI input")
    while ser.in_waiting == 0:
        time.sleep(0.1)
    while ser.in_waiting > 0:
        b = ser.read (1)
        print(b.decode('ascii'), end="")
        if ser.in_waiting == 0:
            time.sleep(0.1) # allow time for SSI to keep up
    print("SSI input cleared")

# ---- ssiSend ---- #

def ssiSend(buf, ser):
    print("Sending data to SSI")
    time.sleep(2) # allow time for SSI to wake up
    ssiEcho(ser);
    count = 0
    for ch in buf:
        print(chr(ch), end='')
        if chr(ch) == '0' or chr(ch) == '1':
            count += 1
        while ser.out_waiting != 0:
            time.sleep (0.01)
        if ser.write (bytes([ch])) != 1:
            sys.stderr.write("ssiupload: ser.write failed\n")
            sys.exit(1)
    print("ssiupload: Buffer sent", count, "bits")

# ---- main program ---- #

parser = argparse.ArgumentParser(
description='Transfer tank 0 image via SSI')
parser.add_argument('file', help='file to upload')
parser.add_argument('-d', '--device', help='serial device',
                     default='/dev/tty.usbmodem141401')
args = parser.parse_args()
#print("Arguments:", args)
devicePath = args.device
filePath = args.file
ssiUpload(filePath, devicePath)