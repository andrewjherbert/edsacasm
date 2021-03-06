
#Transfer EDSAC tank 0 images to SSI  - Andrew Herbert 15/02/2022

# 15/02/2022 changes
# baud rate default set to 19200
# checks for bogus characters in input
# doesn't transmit newlines

# ssiupload device infile

import argparse
import serial
import sys
import time

# ---- ssiUpload ---- #

def ssiUpload (filePath, devicePath, rate):

    # Set up serial port
    ser = serial.Serial()
    ser.port     = devicePath
    ser.baudrate = rate

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

    ssiWait(ser, 30)  # clear any output from SSI
    ssiEcho(ser)

    input("Type RETURN to exit from ssiupload")

    # Close the serial port
    ser.close()

# ---- ssiWait ----#

def ssiWait(ser, secs):
    # print("Waiting for SSI input")
    for ticks in range(secs*1000):
        if ser.in_waiting == 0:
            time.sleep(0.001)
        else:
            return
        
# ---- ssiEcho ---- #

def ssiEcho(ser):
    # echo any messages coming back
    print("Looking for SSI input")
    while ser.in_waiting > 0:
        b = ser.read (1)
        print(b.decode('utf-8'), end="")
        # wait up to 2 secs for output to come
        ticks = 0
        while ser.in_waiting == 0:
            ticks += 1
            if ticks > 2000:
                break
            time.sleep(0.001) # allow time for SSI to keep up
    print("SSI input cleared")

# ---- ssiSend ---- #

def ssiSend(buf, ser):
    # print("Sending data to SSI")
    count = 0
    for ch in buf:
        print(chr(ch), end='')
        if chr(ch) != '0' and chr(ch) != '1' and chr(ch) != '\n':
            print("Error in  input - found \'", chr(ch), "\'")
            sys.exit(1)
        while ser.out_waiting != 0:
            time.sleep (0.005)
        if chr(ch) != '\n':
            if ser.write (bytes([ch])) != 1:
                sys.stderr.write("ssiupload: ser.write failed\n")
                sys.exit(1)
    # print("ssiupload: Buffer sent", count, "bits")

# ---- main program ---- #

parser = argparse.ArgumentParser(
description='Transfer tank 0 image via SSI')
parser.add_argument('file', help='file to upload')
parser.add_argument('-d', '--device', help='serial device',
                     default='/dev/tty.usbmodem141401')
parser.add_argument('-b', '--baud', type=int, help='baud rate',
                    default=19200)
args = parser.parse_args()
#print("Arguments:", args)
devicePath = args.device
filePath = args.file
ssiUpload(filePath, devicePath, args.baud)
