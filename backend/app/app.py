from fastapi import Depends, FastAPI
from database.db import engine,Base
from routers import DS18B20
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.get("/")
def root():
    return "Uvicorn Launched Successfully"


app.include_router(DS18B20.router)


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

