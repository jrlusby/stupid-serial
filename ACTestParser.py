#! /usr/bin/env python2.7
import serial
import sys
import threading
import argparse

dontprint = False

def sending(seri):
    global dontprint
    while True:
        blah = raw_input().strip()
        seri.write(blah)
        seri.flush()

def receiving(seri, ofile):
    while True:
        s = seri.readline()
        if "REPORT" in s:
            with open(ofile, "a") as f:
                f.write(s.strip())
        if not dontprint:
            sys.stdout.write(s)
            sys.stdout.flush()

parser = argparse.ArgumentParser(description="Simple Serial reader / writer")
parser.add_argument('-s', '--serial', dest='serial_port',
        default="/dev/cu.usbmodem1421", help='the serial communication port')
parser.add_argument('-b', '--baudrate', dest='baud_rate',
        default='9600', help='baud rate for the serial communication')
parser.add_argument('outfile', help="file to append report to")
args = parser.parse_args()

try:
    # This is here because of an error in my laptop serial stack or whatever
    ser = serial.Serial(args.serial_port, 9600, timeout=0)
    ser.close()
    ser = serial.Serial(args.serial_port, args.baud_rate, timeout=1)
except:
    print("serial open failure")

t1 = threading.Thread(target=sending, args = (ser,))
t1.daemon = True
t1.start()
try:
    receiving(ser, args.outfile)
except (KeyboardInterrupt, SystemExit):
    print("I Die")
    pass
finally:
    # raise
    ser.close()
