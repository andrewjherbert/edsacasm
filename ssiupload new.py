
#Transfer EDSAC tank 0 images to SSI  - Andrew Herbert 08/02/2021

# ssiupload device infile

import argparse
import serial
import sys
import time

xoff = 19
xon = 17

# ---- ssiUpload ---- #

def ssiUpload (filePath, devicePath, baud):

    # Set up serial port
    ser = serial.Serial()
    ser.port     = devicePath
    ser.baudrate = baud

    # Open serial port
    try:
        # print("Opening", devicePath)
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
    print("SSI unit should have reset\n")

    # clear any input from SSI
    ssiEcho(ser)
    
    input("Select LOCAL mode and type RETURN to continue")

    # clear any input from SSI
    ssiEcho(ser)
    input("Scroll to, but do not select, TEXTFILE and type RETURN to continue")

    # clear any input from SSI
    ssiEcho(ser)
    
    # Send file to SSI
    ssiSend(buf, ser)

    # clear any output from SSI
    ssiEcho(ser) 

    print("Select TEXTFILE to load copy to store")

    ssiWait(ser)  # clear any output from SSI
    ssiEcho(ser)

    input("Type RETURN to exit from ssiupload")

    # Close the serial port
    ser.close()

# ---- ssiWait ----#

def ssiWait(ser):
    # print("Waiting for SSI input")
    for ticks in range(200):
        if ser.in_waiting == 0:
            time.sleep(0.01)
        else:
            return
            
# ---- ssiEcho ---- #

def ssiEcho(ser):
    # echo any messages coming back
    print("Looking for SSI input")
    while ser.in_waiting > 0:
        b = ser.read(1)
        if b != XON and b != XOFF: # ignore XON/OFF
            print(b.decode('ascii'), end="")
        if ser.in_waiting == 0:
            time.sleep(0.1) # allow time for SSI to keep up
    print("SSI input cleared")

# ---- ssiSend ---- #

def ssiSend(buf, ser):
    # print("Sending data to SSI")
    count = 0
    for ch in buf:
        # check for XOFF
        if ser.in_waiting > 0:
            b = ser.read(1)
            if b == 19: # look for XOFF
                while ser.in_waiting == 0:
                    time.sleep(0.005)
                b = ser.read(1)
                if b != 17: # wait for XON
                    print("XOFF not follwed by XON")
                    sys.exit(1)
        print(chr(ch), end='')
        if chr(ch) == '0' or chr(ch) == '1':
            count += 1
        while ser.out_waiting != 0:
            time.sleep (0.005)
        if ser.write (bytes([ch])) != 1:
            sys.stderr.write("ssiupload: ser.write failed\n")
            sys.exit(1)
        else:
            time.sleep(0.005)
    # print("ssiupload: Buffer sent", count, "bits")

# ---- main program ---- #

parser = argparse.ArgumentParser(
description='Transfer tank 0 image via SSI')
parser.add_argument('file', help='file to upload')
parser.add_argument('-d', '--device', type=int, help='serial device',
                     default='/dev/tty.usbmodem141401')
parser.add_argument('-b', '--baud', help='baud rate', default=19200)
args = parser.parse_args()
#print("Arguments:", args)
devicePath = args.device
filePath = args.file
ssiUpload(filePath, devicePath, args.baud)
