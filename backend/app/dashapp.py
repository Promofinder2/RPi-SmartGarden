import dash
from fastapi import Depends
from sqlalchemy.orm.session import Session
from dash.dependencies import Input, Output
from dash import dcc,html
import flask
import pandas as pd
import os
import plotly as plt
import plotly.express as px
os.chdir('backend')
from database import db_DS18B20
from database.models import database_DS18B20
from database.db import get_db
from routers import DS18B20
import asyncio
from typing import List
def fetch_data():
    dbase2 = database_DS18B20.query.all()
    return dbase2

def process_data():

    ds18b20_request = fetch_data()
    ds18b20_request_dict_list = [x.__dict__ for x in ds18b20_request]

    df=pd.DataFrame(ds18b20_request_dict_list)

    fig=px.scatter(df[15::],x='timestamp', y='temperature_Farenheit',facet_col='measurement_id')
    fig.show()


