import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.app:app",host="192.168.50.172",port=8000, log_level="info")

#import pandas
#import pydantic
#import time
#import RPi.GPIO as GPIO
#import os
#import asyncio
#import board
#from adafruit_htu21d import HTU21D
#from fastapi import FastAPI
#from enum import Enum
#from backend.database.models import database_DS18B20
#from backend.routers.schemas import DS18B20
#import datetime
#import importlib
#os.system('sudo modprobe w1-gpio')
#os.system('sudo modprobe w1-therm')
#base_dir = '/sys/bus/w1/devices/'
#sensor_files = []
#for f in os.listdir(base_dir):
#    if '28' in f:
#        device_folder= base_dir+f+'/'
#        sensor_files.append(device_folder+'w1_slave')
#def log_temperature(id):
#    ds18b20 = read_temp()
#    raw_temp = read_temp_raw()
#    probe1_temp =  ds18b20[0] 
#    probe2_temp = ds18b20[1]    
#    timestamp = datetime.datetime.now()
#    timestamp = f'{str(timestamp.hour)}:{str(timestamp.minute)}:{str(timestamp.microsecond)} | {str(timestamp.month)}-{str(timestamp.day)}-{str(timestamp.year)}'
#    print(raw_temp)
#    ds18b20_dict_1 = {
#        "id":id,
#        "timestamp":timestamp,
#        "raw_input":raw_temp,
#        "measurement_id": "Probe 1",
#        "temperature_Celsius" : float(probe1_temp),
#        "temperature_Farenheit" : 42.069,
#    }
#    ds18b20_dict_2 = {
#        "id":id,
#        "timestamp":timestamp,
#        "raw_input":raw_temp,
#        "measurement_id": "Probe 2",
#        "temperature_Celsius" : float(probe2_temp),
#        "temperature_Farenheit" : 42.069,
#    }
#    res1 = DS18B20(**ds18b20_dict_1) 
#    res2 = DS18B20(**ds18b20_dict_2) 
#    return [res1.dict(),res2]
#
#
#def read_temp_htu21d():
#    i2c = board.I2C()
#    sensor = HTU21D(i2c)
#    temp = sensor.temperature
#    hum = sensor.relative_humidity
#
#    return [temp,hum]
#def read_temp_raw():
#    lines = []
#    for sensor in sensor_files:
#        f=open(sensor,'r')
#        lines.append(f.readlines())
#        f.close()
#
#    return lines
#def read_temp():
#    lines = read_temp_raw()
#    temperature_readings=[]
#    for i,line in enumerate(lines):
#        
#        txt=line[1]
#        split_txt = txt.split('t=')
#        probe_temp=split_txt[1][0:5]
#        temperature_readings.append(probe_temp)
#
#    return temperature_readings
#
##GPIO.setmode(GPIO.BOARD)
##GPIO.setup(37,GPIO.OUT)
##GPIO.setup(38,GPIO.OUT)
##GPIO.setup(40,GPIO.OUT)
##
#try:
#    x=0
#    while True:
#
#        output = log_temperature(x)
#        print (type(output[0]))
#        print (type(output[1]))
#
#
#        print(output)
##        htu21d = read_temp_htu21d()
##        ds18b20 = read_temp()
##        htu21d_temp= htu21d[0]
##        htu21d_humidity=htu21d[1]
##
##        probe1_temp =  ds18b20[0] 
##        probe2_temp = ds18b20[1]
##
##        print(f'HTU21D\t\t\t|\tProbe 1\t|\tProbe 2')        
##        print(f'{htu21d_temp}\t|\t{probe1_temp}\t|\t{probe2_temp}')
##        print(htu21d_humidity)
##        print('\n\n')
#        time.sleep(.2)
## #       print('heyoooo....turn on relay')
# #       GPIO.output(37,True)
# #       time.sleep(2)
# #       print('relay 2 off')
# #       GPIO.output(40,True)
# #       GPIO.output(38,False)
# #       time.sleep(1)
# #       print('listen what i sayyyy ooooooo ooooo.... turn off relay')
# #       GPIO.output(37,False)
# #       time.sleep(1)
# #       print('relay 2 on')
# #       GPIO.output(38,True)
# #       GPIO.output(40,False)
# #       print(read_temp_raw())
# # 
#    x+=1       
#except KeyboardInterrupt:
#    print('\n**Exit Success')
#finally:
#    GPIO.cleanup()
#  #  print(dir(GPIO))
#    print('\nFinally Success')