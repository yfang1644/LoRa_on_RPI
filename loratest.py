#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import serial
import time
    
CFG_REG = [b'\xC2\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00',
           b'\xC2\x00\x09\x00\x00\x00\x62\x00\x17\x03\x00\x00']
RET_REG = [b'\xC1\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00',
           b'\xC1\x00\x09\x00\x00\x00\x62\x00\x17\x03\x00\x00']

ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flushInput()
ser.write(CFG_REG[0])
time.sleep(1)
r_buff = ser.read(ser.inWaiting())
print("monitor message:", r_buff)
