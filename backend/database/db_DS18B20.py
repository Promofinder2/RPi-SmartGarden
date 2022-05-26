from fastapi import HTTPException, status
from routers.schemas import DS18B20
from sqlalchemy.orm.session import Session
from .models import database_DS18B20
import datetime

def create(db:Session, request: database_DS18B20):
    new_readings = database_DS18B20(
        timestamp = request.timestamp,
        raw_input = request.raw_input,
        measurement_id = request.measurement_id,
        temperature_Celsius = request.temperature_Celsius,
        temperature_Farenheit = request.temperature_Farenheit
    )
    db.add(new_readings)
    db.commit()
    db.refresh(new_readings)
    return new_readings

def get_all(db:Session):
    query_response =db.query(database_DS18B20).all() 
    return query_response



    