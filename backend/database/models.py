from multiprocessing.dummy import Array
import pydantic
from datetime import datetime
from typing import Optional,List
from .db import Base
from sqlalchemy import Column, Integer, String, DateTime,Float,ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.types import PickleType


class database_DS18B20(Base):
    __table_args__ = {'extend_existing':True}
    __tablename__ = 'DS18B20_TEMPERATURE_SENSOR'
    id=Column(Integer,primary_key=True,index=True)

    timestamp = Column( String)
    raw_input =Column( PickleType)
    measurement_id =Column( String)
    temperature_Celsius =Column( Float)
    temperature_Farenheit =Column( Float)


class database_HTU21D(Base):
    __tablename__ = "HTU21D_TEMPERATURE_HUMIDITY_SENSOR"
    __table_args__ = {'extend_existing':True}
    id=Column(Integer,primary_key=True,index=True)
    timestamp =Column( String)
    measurement_id =Column( String)
    temperature_Farenheit =Column( Float)
    relative_humidity =Column( Float)

#class database_Relay(Base):
#    
#    relay_id_number : int
#    status : bool


