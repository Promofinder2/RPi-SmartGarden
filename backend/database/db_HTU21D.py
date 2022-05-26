from fastapi import HTTPException, status
from routers.schemas import HTU21D
from sqlalchemy.orm.session import Session
from database.models import database_HTU21D
import datetime

def create(db:Session, request: database_HTU21D):
    new_readings = database_HTU21D(
        timestamp = request.timestamp,
        measurement_id = request.measurement_id,
        temperature_Farenheit = request.temperature_Farenheit,
        relative_humidity = request.relative_humidity
    )
    db.add(new_readings)
    db.commit()
    db.refresh(new_readings)
    return new_readings

def get_all(db:Session):
    query_response =db.query(database_HTU21D).all() 
    return query_response

