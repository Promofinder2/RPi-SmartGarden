from fastapi import APIRouter, status, Depends, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from routers.schemas import DS18B20
from database.db import get_db
from database import db_DS18B20
import shutil
from typing import List
import os
import RPi.GPIO as GPIO
import board
from adafruit_htu21d import HTU21D
import datetime
from enum import Enum
import asyncio
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



router = APIRouter(
    prefix='/sensor_readings',
    tags = ['Temperature']
)

@router.post('')
async def create(db: Session = Depends(get_db)):
    res1,res2 = await log_temperature()
    for reading in [res1,res2]:
        db_DS18B20.create(db,reading)
    


@router.get('/all',response_model=List[DS18B20])
async def readings(db: Session= Depends(get_db)):
    res1,res2 = await log_temperature()
    dbase = db_DS18B20.get_all(db)
    dbase.append(res1)
    dbase.append(res2)
    return dbase


async def log_temperature():
    ds18b20 = read_temp()
    raw_temp = read_temp_raw()
    probe1_temp =  float(ds18b20[0])/1000.0
    probe2_temp = float(ds18b20[1])/1000.0    
    timestamp = datetime.datetime.now()
    timestamp = f'{str(timestamp.hour)}:{str(timestamp.minute)}:{str(timestamp.microsecond)} | {str(timestamp.month)}-{str(timestamp.day)}-{str(timestamp.year)}'
    ds18b20_dict_1 = {
        "timestamp":timestamp,
        "raw_input":raw_temp,
        "measurement_id": "Probe 1",
        "temperature_Celsius" : float(probe1_temp),
        "temperature_Farenheit" : (float(probe1_temp)*1.8)+32.0,
    }
    ds18b20_dict_2 = {
        "timestamp":timestamp,
        "raw_input":raw_temp,
        "measurement_id": "Probe 2",
        "temperature_Celsius" : float(probe2_temp),
        "temperature_Farenheit" : (float(probe2_temp)*1.8)+32.0,
    }
    res1 = DS18B20(**ds18b20_dict_1) 
    res2 = DS18B20(**ds18b20_dict_2)     
    return [res1,res2]




