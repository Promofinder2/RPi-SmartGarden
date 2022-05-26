from fastapi import Depends, FastAPI
from database.db import engine,Base,get_db
from routers import DS18B20,HTU21D
from database.models import database_DS18B20,database_HTU21D
from database import db_DS18B20,db_HTU21D
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from fastapi_utils.session import FastAPISessionMaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sensor_database.db?check_same_thread=False'
sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)
app=FastAPI()


app.include_router(DS18B20.router)
app.include_router(HTU21D.router)


@app.on_event("startup")
@repeat_every(seconds=60*.5,wait_first=False)
async def take_ds18b20_readings() -> None:
    res1,res2 = await DS18B20.log_temperature()
    with sessionmaker.context_session() as db:
        for reading in [res1,res2]:
            db_DS18B20.create(db=db,request=reading)

@app.on_event("startup")
@repeat_every(seconds=60*.5,wait_first=False)
async def take_htu21d_readings() -> None:
    res = await HTU21D.log_temperature_humidity()
    with sessionmaker.context_session() as db:
        for reading in [res]:
            db_HTU21D.create(db=db,request=reading)


origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods='*',
    allow_headers=['*']
)

Base.metadata.create_all(engine)

