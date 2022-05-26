import dash
from fastapi import Depends
from sqlalchemy.orm.session import Session
from dash.dependencies import Input, Output
from dash import dcc,html
import importlib
import flask
import pandas as pd
import os
os.chdir('backend')
import plotly as plt
import plotly.express as px
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
    return fig


global fig
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgp.css']
Dapp=dash.Dash(__name__,external_stylesheets=external_stylesheets)

def serve_layout():
    fig=process_data()
    return html.Div(children=[
html.H1("SMART GARDEN V0.1",style={'text-align':'center'}),
html.H3("DS18B20 TEMPERATURE PROBE READINGS",style={'text-align':'center'}),
dcc.Graph(figure=fig)
])

Dapp.layout= serve_layout
if __name__ == '__main__':

    Dapp.run_server("192.168.50.172",8050,debug=False)

