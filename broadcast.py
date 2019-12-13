#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import serial
import time
import threading
    
class MyThread(threading.Thread):
    def __init__(self, arg):
        super(MyThread, self).__init__()
        self.port = arg[0]
        self.mesg = arg[1]

    def run(self):
        while True:
            time.sleep (2)
            self.port.write(self.mesg)
            print ("xxx")

M0, M1 = 22, 27

CFG_REG = b'\xC2\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00'
RET_REG = b'\xC1\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup((M0, M1), GPIO.OUT)

GPIO.output((M0, M1), (GPIO.LOW, GPIO.HIGH))
time.sleep(0.01)

ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flushInput()
if ser.isOpen():
    print("It's setting BROADCAST and MONITOR mode")
    ser.write(CFG_REG)
    time.sleep(0.1)
    r_buff = ser.read(ser.inWaiting())
    if r_buff == RET_REG:
        print("BROADCAST and MONITOR mode was actived")
        GPIO.output((M0, M1), (GPIO.LOW, GPIO.LOW))

    t1 = MyThread((ser, "This is a BROADCAST message\r\n".encode()))
else:
    print ("Device open error.")
    GPIO.cleanup()
    exit()

t1.start()
while True:
    if ser.inWaiting() > 0:
        time.sleep(0.1)
        r_buff = ser.read(ser.inWaiting())
        if r_buff != "":
            print("monitor message:", r_buff)

if ser.isOpen():
    ser.close()
GPIO.cleanup()
