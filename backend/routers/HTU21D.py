import datetime
import RPi.GPIO as GPIO
import os
import board
from adafruit_htu21d import HTU21D as htu21d_sensor
from fastapi import APIRouter, status, Depends, UploadFile
from fastapi_utils.tasks import repeat_every
from routers.schemas import HTU21D
from typing import Optional , List
from database.db import get_db
from database import db_HTU21D
from sqlalchemy.orm import Session



def read_temp_htu21d():
    i2c = board.I2C()
    sensor = htu21d_sensor(i2c)
    temp = sensor.temperature
    hum = sensor.relative_humidity

    return [temp,hum]

router = APIRouter(
    prefix = '/HTU21D',
    tags = ['Temperature','Relative_Humidity']
)

@router.post('')
async def create (db: Session = Depends(get_db)):
    res = await log_temperature_humidity()
    for reading in [res]:

        db_HTU21D.create(db, reading)


@router.get('/all',response_model=List[HTU21D])
async def readings(db: Session=Depends(get_db)):
    res = await log_temperature_humidity()
    dbase= db_HTU21D.get_all(db)
    dbase.append(res)
    return dbase

async def log_temperature_humidity():
    htu21d_measurements = read_temp_htu21d()
    timestamp = datetime.datetime.now()
    timestamp = f'{str(timestamp.hour)}:{str(timestamp.minute)}:{str(timestamp.microsecond)} | {str(timestamp.month)}-{str(timestamp.day)}-{str(timestamp.year)}'
    htu21d_dict_1 = {
        "timestamp":timestamp,
        "measurement_id": "HTU21D_TEMP_HUMIDITY_SENSOR",
        "temperature_Farenheit" : (float(htu21d_measurements[0])*1.8)+32.0,
        "relative_humidity" : float(htu21d_measurements[1])
    }
    measurement_response = HTU21D(**htu21d_dict_1)
    return measurement_response