
# Transfer EDSAC tank 0 images to SSI  - Andrew Herbert 10/08/2022

# 01/11/2022 changes
# Support ACK/NOACK during transfer to SSI

# 15/02/2022 changes
# baud rate default set to 19200
# checks for bogus characters in input
# doesn't transmit newlines

# ssiupload device infile

import argparse
import serial
import sys
import time

dataRate = 19200
XON = 17
XOFF = 19

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
    input("Reset SSI unit and type RETURN to continue\n")

    # clear any input from SSI
    ssiWait(ser, 1)
    #ssiEcho(ser)
    print("Select LOCAL mode if on SSI at Rack F2, or REMOTE mode, tank 0",
           "if at Rack M3")
    input("Scroll to, but do not select, TEXTFILE and type RETURN to continue")

    # Send file to SSI
    ssiSend(buf, ser)

    # clear any output from SSI
    ssiWait(ser, 5)
    ssiEcho(ser)

    print("Select TEXTFILE to load copy to store")

    # clear residual output from SSI
    ssiWait(ser, 10)
    ssiEcho(ser)

    # Close the serial port
    ser.close()

# ---- ssiWait ----#

def ssiWait(ser, secs):
    # print("ssiWait: waiting up to", secs, "secs to see if any output from SSI")
    for i in range(secs):
        if ser.in_waiting == 0:
            time.sleep(1)
        else:
            return
    print("ssiWait timed out after", secs, "secs; no output detected")

# ---- ssiEcho ---- #

def ssiEcho(ser):
    # echo any messages coming back
    count = 0
    print("ssiEcho: show any output from SSI")
    while ser.in_waiting > 0:
        count += 1
        b = ser.read(1)
        if b == XOFF:
            # wait for XON
            print("+", end="")
            b = ser.read(1)
            if b[0] != XON:
                print("XOFF not followed by XON, instead found code", b[0])
                sys.exit(1)
            else:
                print("-", end="")
        elif b[0] == XON:
            pass #print("X", end="")
        else:
            print(chr(b[0]), end="")
        # wait up to 2 secs for output to come
        ticks = 0
        while ser.in_waiting == 0:
            ticks += 1
            if ticks > 2000:
                print("\nssiEcho: no more output received after waiting 2 seconds")
                return
            time.sleep(0.001) # allow time for SSI to keep up
    if count > 0:
        print('ssiEcho read', count, 'chars')
    else:
        print('ssiEcho found nothing to read')

# ---- ssiSend ---- #

def ssiSend(buf, ser):
    print('ssiSend starting')
    chars = 0
    bits = 0
    xons = 0
    for ch in buf:
        print(chr(ch), end='')
        if chr(ch) != '0' and chr(ch) != '1' and chr(ch) != '\n':
            print("ssiSend: Error in  file to upload - found \'", chr(ch), "\'")
            sys.exit(1)
        # look to see if any output from SSI
        while ser.in_waiting != 0:
            b = ser.read(1)
            # check to see if XOFF/XON sequence
            if b[0] == XOFF:
                # wait for XON
                b = ser.read(1)
                if b[0] != XON:
                    print('ssiSend: XON not followed by XOFF, instead found code', b[0])
                    sys.exit(1)
                else:
                    print("-X+")
            elif b[0] == XON:
                xons += 1
            else:
                print("'"+chr(b[0])+"'")
        # Now send character to SSI
        if ser.write (bytes([ch])) == 1: # output binary digit
            chars += 1 # character transmitted
            if ch == ord('0') or ch == ord('1'):
                bits += 1 # and character was a bit (0 or 1)
        else:
            sys.stderr.write("ssiupload: ser.write failed\n")
            sys.exit(1)
    print("ssiSend: Buffer of size", len(buf), "sent as", chars, "chars containing",
          bits, "bits,", xons, "XONs received")

# ---- main program ---- #

parser = argparse.ArgumentParser(
description='Transfer tank 0 image via SSI')
parser.add_argument('file', help='file to upload')
parser.add_argument('-d', '--device', help='serial device',
                     default='/dev/tty.usbmodem141401')
parser.add_argument('-b', '--baud', type=int, help='baud rate',
                    default=dataRate)
args = parser.parse_args()
#print("Arguments:", args)
devicePath = args.device
filePath = args.file
ssiUpload(filePath, devicePath, args.baud)
