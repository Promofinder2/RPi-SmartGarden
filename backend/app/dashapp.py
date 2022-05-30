from asyncore import read
import threading
import time
time.sleep(2)
import sys
sys.path.append('/home/pi/github-Projects/RPi-SmartGarden/RPi-SmartGarden/backend/')
import dash
from fastapi import Depends
from sqlalchemy.orm.session import Session
from dash.dependencies import Input, Output
from dash import dcc,html
import importlib
import flask
import pandas as pd
import os
import plotly as plt
import plotly.express as px
from database import db_DS18B20
from database.models import database_DS18B20,database_HTU21D
import cv2
from database.db import get_db
from routers import DS18B20
import asyncio
from quart import Quart, websocket
from typing import List
import base64
import threading
from dash_extensions import WebSocket
global cap
global ret
global img
delay_between_frames=0.05
server = Quart(__name__)

@server.websocket("/stream")
async def stream_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    while True:
        try:
            if delay_between_frames is not None:
                await asyncio.sleep(delay=delay_between_frames)
            frame = cap.get_frame()
            await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")
        except AssertionError as e:
            print(e)




def fetch_data_ds18b20():
    dbase2 = database_DS18B20.query.all()
    return dbase2
def process_data_ds18b20():

    ds18b20_request = fetch_data_ds18b20()
    ds18b20_request_dict_list = [x.__dict__ for x in ds18b20_request]

    df=pd.DataFrame(ds18b20_request_dict_list)

    fig=px.line(df[15::],x='timestamp', y='temperature_Farenheit',facet_col='measurement_id')
    return fig


def fetch_data_htu21d():
    dbase2 = database_HTU21D.query.all()
    return dbase2
def process_data_htu21d():

    htu21d_request = fetch_data_htu21d()
    htu21d_request_dict_list = [x.__dict__ for x in htu21d_request]

    df=pd.DataFrame(htu21d_request_dict_list)

    fig=px.line(df[15::],x='timestamp', y=['temperature_Farenheit','relative_humidity'],facet_col='measurement_id')
    return fig
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgp.css']
Dapp=dash.Dash(__name__,external_stylesheets=external_stylesheets)

def serve_layout():
    fig=process_data_ds18b20()
    return html.Div(children=[
html.H1("SMART GARDEN V0.1",style={'text-align':'center'}),
html.H3("DS18B20 TEMPERATURE PROBE READINGS",style={'text-align':'center'}),
dcc.Graph(figure=fig),html.H3("HTU21D TEMPERATURE HUMIDITY SENSOR READINGS",style={'text-align':'center'}),
dcc.Graph(figure=process_data_htu21d()),
html.H2("Streaming",style={'text-align':'center'}),
html.Img(id='video_stream'), WebSocket(url=f"ws://127.0.0.1:5000/stream",id="ws")
])

Dapp.layout= serve_layout
Dapp.clientside_callback("function(m){return m? m.data : '';}",Output(f"video_stream","src"), Input(f"ws","message"))

if __name__ == '__main__':

    Dapp.run_server("192.168.50.172",8050,debug=False)

