import pydantic
from datetime import datetime
from typing import Optional,List

class DS18B20(pydantic.BaseModel):
    timestamp : Optional[str]
    raw_input : List[List[str]]
    measurement_id : Optional[str]
    temperature_Celsius : Optional[float]
    temperature_Farenheit : Optional[float]
    class Config():
        orm_mode=True
class HTU21D(pydantic.BaseModel):
    timestamp : Optional[str]
    measurement_id : Optional[str]
    temperature_Celcius : Optional[float]
    temperature_Farenheit : Optional[float]
    relative_humidity : Optional[float]
    class Config():
        orm_mode=True
class Relay(pydantic.BaseModel):
    relay_id_number : int
    status : bool
    class Config():
        orm_mode=True