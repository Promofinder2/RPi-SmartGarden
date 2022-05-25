import pandas
import pydantic

import time
import RPi.GPIO as GPIO
import os
import board
from adafruit_htu21d import HTU21D


import glob

dir(time.time())

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
sensor_files = []
for f in os.listdir(base_dir):
    if '28' in f:
        device_folder= base_dir+f+'/'
        sensor_files.append(device_folder+'w1_slave')
def read_temp_htu21d():
    i2c = board.I2C()
    sensor = HTU21D(i2c)
    temp = sensor.temperature
    hum = sensor.relative_humidity

    return [temp,hum]
def read_temp_raw():
    lines = []
    for sensor in sensor_files:
        f=open(sensor,'r')
        lines.append(f.readlines())
        f.close()

    return lines
def read_temp():
    lines = read_temp_raw()
    temperature_readings=[]
    for i,line in enumerate(lines):
        
        txt=line[1]
        split_txt = txt.split('t=')
        probe_temp=split_txt[1][0:5]
        temperature_readings.append(probe_temp)

    return temperature_readings

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(37,GPIO.OUT)
#GPIO.setup(38,GPIO.OUT)
#GPIO.setup(40,GPIO.OUT)
#
try:
    while True:
        htu21d = read_temp_htu21d()
        ds18b20 = read_temp()
        htu21d_temp= htu21d[0]
        htu21d_humidity=htu21d[1]

        probe1_temp =  ds18b20[0] 
        probe2_temp = ds18b20[1]

        print(f'HTU21D\t\t\t|\tProbe 1\t|\tProbe 2')        
        print(f'{htu21d_temp}\t|\t{probe1_temp}\t|\t{probe2_temp}')
        print(htu21d_humidity)
        print('\n\n')
        time.sleep(.2)
 #       print('heyoooo....turn on relay')
 #       GPIO.output(37,True)
 #       time.sleep(2)
 #       print('relay 2 off')
 #       GPIO.output(40,True)
 #       GPIO.output(38,False)
 #       time.sleep(1)
 #       print('listen what i sayyyy ooooooo ooooo.... turn off relay')
 #       GPIO.output(37,False)
 #       time.sleep(1)
 #       print('relay 2 on')
 #       GPIO.output(38,True)
 #       GPIO.output(40,False)
 #       print(read_temp_raw())        
except KeyboardInterrupt:
    print('\n**Exit Success')
finally:
    GPIO.cleanup()
  #  print(dir(GPIO))
    print('\nFinally Success')